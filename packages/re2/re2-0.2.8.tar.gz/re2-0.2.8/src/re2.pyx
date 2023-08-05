# cython: infer_types(False)
# Import re flags to be compatible.
import sys
import re
I = re.I
IGNORECASE = re.IGNORECASE
M = re.M
MULTILINE = re.MULTILINE
S = re.S
DOTALL = re.DOTALL
U = re.U
UNICODE = re.UNICODE
X = re.X
VERBOSE = re.VERBOSE

FALLBACK_QUIETLY = 0
FALLBACK_WARNING = 1
FALLBACK_EXCEPTION = 2

VERSION = (0, 2, 8)
VERSION_HEX = 0x000208

cdef int current_notification = FALLBACK_WARNING

def set_fallback_notification(level):
    """
    Set the fallback notification to a level; one of:
        FALLBACK_QUIETLY
	FALLBACK_WARNING
	FALLBACK_EXCEPTION
    """
    global current_notification
    level = int(level)
    if level < 0 or level > 2:
        raise ValueError("This function expects a valid notification level.")
    current_notification = level


class RegexError(re.error):
    """
    Some error has occured in compilation of the regex.
    """
    pass

cdef int _I = I, _M = M, _S = S, _U = U, _X = X

cimport _re2
cimport python_unicode
from cython.operator cimport preincrement as inc, dereference as deref
import warnings

cdef object cpp_to_pystring(_re2.cpp_string input):
    # This function is a quick converter from a std::string object
    # to a python string. By taking the slice we go to the right size,
    # despite spurious or missing null characters.
    return input.c_str()[:input.length()]

cdef inline object cpp_to_utf8(_re2.cpp_string input):
    # This function converts a std::string object to a utf8 object.
    return python_unicode.PyUnicode_DecodeUTF8(input.c_str(), input.length(), 'strict')

cdef inline object char_to_utf8(_re2.const_char_ptr input, int length):
    # This function converts a C string to a utf8 object.
    return python_unicode.PyUnicode_DecodeUTF8(input, length, 'strict')

cdef inline object unicode_to_bytestring(object pystring, int * encoded):
    # This function will convert a utf8 string to a bytestring object.
    if python_unicode.PyUnicode_Check(pystring):
        pystring = python_unicode.PyUnicode_EncodeUTF8(python_unicode.PyUnicode_AS_UNICODE(pystring),
                                                       python_unicode.PyUnicode_GET_SIZE(pystring),
                                                       "strict")
        encoded[0] = 1
    else:
        encoded[0] = 0
    return pystring

cdef inline int pystring_to_bytestring(object pystring, char ** cstring, Py_ssize_t * length):
    # This function will convert a pystring to a bytesstring, placing
    # the char * in cstring, and the length in length.
    # First it will try treating it as a str object, but failing that
    # it will move to utf-8. If utf8 does not work, then it has to be
    # a non-supported encoding.
    return _re2.PyObject_AsCharBuffer(pystring, <_re2.const_char_ptr*> cstring, length)


cdef class Match:
    cdef _re2.StringPiece * matches
    cdef _re2.const_stringintmap * named_groups

    cdef bint encoded
    cdef object _lastgroup
    cdef int _lastindex
    cdef int nmatches
    cdef object match_string
    cdef tuple _groups
    cdef dict _named_groups

    def __init__(self):
        self._lastgroup = -1
        self._lastindex = -1
        self._groups = None

    cdef init_groups(self):
        cdef list groups = []
        cdef int i
        cdef bint cur_encoded = self.encoded

        if self._groups is not None:
            return

        for i in range(self.nmatches):
            if self.matches[i].data() == NULL:
                groups.append(None)
            else:
                if cur_encoded:
                    groups.append(char_to_utf8(self.matches[i].data(), self.matches[i].length()))
                else:
                    groups.append(self.matches[i].data()[:self.matches[i].length()])
        self._lastindex = len(groups) - 1
        self._groups = tuple(groups)

    def groups(self):
        self.init_groups()
        return self._groups[1:]

    def group(self, groupnum=0):
        cdef int idx

        self.init_groups()

        if isinstance(groupnum, basestring):
            return self.groupdict()[groupnum]

        idx = groupnum

        if idx > self.nmatches - 1:
            raise IndexError("no such group")
        return self._groups[idx]

    cdef _makespan(self, int groupnum=0):
        cdef int start, end
        cdef _re2.StringPiece * piece
        cdef char * s = self.match_string
        if groupnum > self.nmatches - 1:
            raise IndexError("no such group")
        piece = &self.matches[groupnum]
        if piece.data() == NULL:
            return (-1, -1)
        start = piece.data() - s
        end = start + piece.length()
        return (start, end)

    def expand(self, object template):
        # TODO - This can be optimized to work a bit faster in C.
        # Expand a template with groups
        items = template.split('\\')
        for i, item in enumerate(items[1:]):
            if item[0].isdigit():
                # Number group
                if item[0] == '0':
                    items[i + 1] = '\x00' + item[1:]
                else:
                    items[i + 1] = self.group(int(item[0])) + item[1:]
            elif item[:2] == 'g<' and '>' in item:
                # This is a named group
                name, rest = item[2:].split('>', 1)
                items[i + 1] = self.group(name) + rest
            else:
                # This isn't a template at all
                items[i + 1] = '\\' + item
        return ''.join(items)

    def groupdict(self):
        cdef _re2.stringintmapiterator it
        cdef dict result = {}

        self.init_groups()

        if self._named_groups:
            return self._named_groups

        self._named_groups = result
        it = self.named_groups.begin()
        self._lastgroup = None
        while it != self.named_groups.end():
            result[cpp_to_pystring(deref(it).first)] = self._groups[deref(it).second]
            self._lastgroup = cpp_to_pystring(deref(it).first)
            inc(it)

        return result

    def end(self, int groupnum=0):
        return self._makespan(groupnum)[1]

    def start(self, int groupnum=0):
        return self._makespan(groupnum)[0]

    def span(self, int groupnum=0):
        return self._makespan(groupnum)

    property lastindex:
        def __get__(self):
            if self._lastindex < 1:
                return None
            else:
                return self._lastindex

    property lastgroup:
        def __get__(self):
            if self._lastgroup == -1:
                self.groupdict()
            return self._lastgroup


cdef class Pattern:
    cdef _re2.RE2 * re_pattern
    cdef int ngroups
    cdef bint encoded
    cdef public object pattern

    cdef _search(self, string, int pos, int endpos, _re2.re2_Anchor anchoring):
        """
        Scan through string looking for a match, and return a corresponding
        Match instance. Return None if no position in the string matches.
        """
        cdef Py_ssize_t size
        cdef int result
        cdef char * cstring
        cdef int encoded = 0
        cdef _re2.StringPiece * sp
        cdef _re2.StringPiece * matches = _re2.new_StringPiece_array(self.ngroups + 1)
        cdef Match m = Match()

        string = unicode_to_bytestring(string, &encoded)
        if pystring_to_bytestring(string, &cstring, &size) == -1:
            raise TypeError("expected string or buffer")

        if endpos != -1 and endpos < size:
            size = endpos

        sp = new _re2.StringPiece(cstring, size)
        with nogil:
            result = self.re_pattern.Match(sp[0], <int>pos, anchoring, matches, self.ngroups + 1)

        del sp
        if result == 0:
            return None
        m.matches = matches
        m.encoded = <bint>(encoded) or self.encoded
        m.named_groups = _re2.addressof(self.re_pattern.NamedCapturingGroups())
        m.nmatches = self.ngroups + 1
        m.match_string = string
        return m


    def search(self, string, int pos=0, int endpos=-1):
        """
        Scan through string looking for a match, and return a corresponding
        Match instance. Return None if no position in the string matches.
        """
        return self._search(string, pos, endpos, _re2.UNANCHORED)


    def match(self, string, int pos=0, int endpos=-1):
        """
        Matches zero or more characters at the beginning of the string.
        """
        return self._search(string, pos, endpos, _re2.ANCHOR_START)

    cdef _print_pattern(self):
        cdef _re2.cpp_string * s
        s = <_re2.cpp_string *>_re2.addressofs(self.re_pattern.pattern())
        print cpp_to_pystring(s[0]) + "\n"
        sys.stdout.flush()


    cdef _finditer(self, object string, int pos=0, int endpos=-1, int as_match=0):
        cdef Py_ssize_t size
        cdef int result
        cdef char * cstring
        cdef _re2.StringPiece * sp
        cdef _re2.StringPiece * matches
        cdef Match m
        cdef list resultlist = []
        cdef int encoded = 0

        string = unicode_to_bytestring(string, &encoded)
        if pystring_to_bytestring(string, &cstring, &size) == -1:
            raise TypeError("expected string or buffer")
        encoded = <bint>encoded or self.encoded

        if endpos != -1 and endpos < size:
            size = endpos

        sp = new _re2.StringPiece(cstring, size)

        while True:
            with nogil:
                matches = _re2.new_StringPiece_array(self.ngroups + 1)
                result = self.re_pattern.Match(sp[0], <int>pos, _re2.UNANCHORED, matches, self.ngroups + 1)
            if result == 0:
                break
            # offset the pos to move to the next point
            pos = matches[0].data() - cstring + matches[0].length()
            m = Match()
            m.encoded = encoded
            m.matches = matches
            m.named_groups = _re2.addressof(self.re_pattern.NamedCapturingGroups())
            m.nmatches = self.ngroups + 1
            m.match_string = string
            if as_match:
                if self.ngroups > 1:
                    resultlist.append(m.groups())
                else:
                    resultlist.append(m.group(self.ngroups - 1))
            else:
                resultlist.append(m)
        del sp
        return resultlist

    def finditer(self, object string, int pos=0, int endpos=-1):
        """
        Return all non-overlapping matches of pattern in string as a list
        of match objects.
        """
        # FIXME should return an iterator according to spec
        return self._finditer(string, pos, endpos, 0)

    def findall(self, object string, int pos=0, int endpos=-1):
        """
        Return all non-overlapping matches of pattern in string as a list
        of strings.
        """
        return self._finditer(string, pos, endpos, 1)

    def split(self, string, int maxsplit=0):
        """
        split(string[, maxsplit = 0]) --> list
        Split a string by the occurances of the pattern.
        """
        cdef Py_ssize_t size
        cdef int num_groups = 1
        cdef int result
        cdef int endpos
        cdef int pos = 0
        cdef int num_split = 0
        cdef char * cstring
        cdef _re2.StringPiece * sp
        cdef _re2.StringPiece * matches
        cdef Match m
        cdef list resultlist = []
        cdef int encoded = 0

        if maxsplit < 0:
            maxsplit = 0

        string = unicode_to_bytestring(string, &encoded)
        if pystring_to_bytestring(string, &cstring, &size) == -1:
            raise TypeError("expected string or buffer")

        encoded = <bint>encoded or self.encoded

        if self.ngroups > 0:
            matches = _re2.new_StringPiece_array(2)
            num_groups = 2
        else:
            matches = _re2.new_StringPiece_array(1)

        sp = new _re2.StringPiece(cstring, size)

        while True:
            with nogil:
                result = self.re_pattern.Match(sp[0], <int>pos, _re2.UNANCHORED, matches, num_groups)
            if result == 0:
                break

            endpos = matches[0].data() - cstring
            if encoded:
                resultlist.append(char_to_utf8(&sp.data()[pos], endpos - pos))
            else:
                resultlist.append(sp.data()[pos:endpos])
            # offset the pos to move to the next point
            pos = endpos + matches[0].length()
            if num_groups == 2:
                if encoded:
                    resultlist.append(char_to_utf8(matches[1].data(), matches[1].length()))
                else:
                    resultlist.append(matches[1].data()[:matches[1].length()])

            num_split += 1
            if maxsplit and num_split >= maxsplit:
                break

        if encoded:
            resultlist.append(char_to_utf8(&sp.data()[pos], sp.length() - pos))
        else:
            resultlist.append(sp.data()[pos:])
        del matches
        del sp
        return resultlist

    def sub(self, repl, string, int count=0):
        """
        sub(repl, string[, count = 0]) --> newstring
        Return the string obtained by replacing the leftmost non-overlapping
        occurrences of pattern in string by the replacement repl.
        """
        return self.subn(repl, string, count)[0]

    def subn(self, repl, string, int count=0):
        """
        subn(repl, string[, count = 0]) --> (newstring, number of subs)
        Return the tuple (new_string, number_of_subs_made) found by replacing
        the leftmost non-overlapping occurrences of pattern with the
        replacement repl.
        """
        cdef Py_ssize_t size
        cdef char * cstring
        cdef _re2.StringPiece * sp
        cdef _re2.cpp_string * input_str
        cdef total_replacements = 0
        cdef int encoded = 0

        if callable(repl):
            # This is a callback, so let's use the custom function
            return self._subn_callback(repl, string, count)

        string = unicode_to_bytestring(string, &encoded)
        repl = unicode_to_bytestring(repl, &encoded)
        if pystring_to_bytestring(repl, &cstring, &size) == -1:
            raise TypeError("expected string or buffer")
        encoded = <bint>encoded or self.encoded

        sp = new _re2.StringPiece(cstring, size)
        input_str = new _re2.cpp_string(string)
        if not count:
            total_replacements = _re2.pattern_GlobalReplace(input_str,
                                                            self.re_pattern[0],
                                                            sp[0])
        elif count == 1:
            total_replacements = _re2.pattern_Replace(input_str,
                                                      self.re_pattern[0],
                                                      sp[0])
        else:
            raise NotImplementedError("So far pyre2 does not support custom replacement counts")

        if encoded:
            return (cpp_to_utf8(input_str[0]), total_replacements)
        else:
            return (cpp_to_pystring(input_str[0]), total_replacements)

    def _subn_callback(self, callback, string, int count=0):
        """
        This function is probably the hardest to implement correctly.
        This is my first attempt, but if anybody has a better solution, please help out.
        """
        cdef Py_ssize_t size
        cdef int result
        cdef int endpos
        cdef int pos = 0
        cdef int encoded = 0
        cdef int num_repl = 0
        cdef char * cstring
        cdef _re2.StringPiece * sp
        cdef _re2.StringPiece * matches
        cdef Match m
        cdef list resultlist = []

        if maxsplit < 0:
            maxsplit = 0

        string = unicode_to_bytestring(string, &encoded)
        if pystring_to_bytestring(string, &cstring, &size) == -1:
            raise TypeError("expected string or buffer")
        encoded = <bint>encoded or self.encoded

        sp = new _re2.StringPiece(cstring, size)

        while True:
            with nogil:
                matches = _re2.new_StringPiece_array(self.ngroups + 1)
                result = self.re_pattern.Match(sp[0], <int>pos, _re2.UNANCHORED, matches, self.ngroups + 1)
            if result == 0:
                break

            endpos = matches[0].data() - cstring
            if encoded:
                resultlist.append(char_to_utf8(&sp.data()[pos], endpos - pos))
            else:
                resultlist.append(sp.data()[pos:endpos])
            pos = endpos + matches[0].length()

            m = Match()
            m.encoded = encoded
            m.matches = matches
            m.named_groups = _re2.addressof(self.re_pattern.NamedCapturingGroups())
            m.nmatches = self.ngroups + 1
            m.match_string = string
            resultlist.append(callback(m) or '')

            num_repl += 1
            if count and num_repl >= count:
                break

        if encoded:
            resultlist.append(char_to_utf8(&sp.data()[pos], sp.length() - pos))
        else:
            resultlist.append(sp.data()[pos:])
        del matches
        del sp
        if encoded:
            return (u''.join(resultlist), num_repl)
        else:
            return (''.join(resultlist), num_repl)


def compile(pattern, int flags=0):
    """
    Compile a regular expression pattern, returning a pattern object.
    """
    cdef char * string
    cdef Py_ssize_t length
    cdef _re2.StringPiece * s
    cdef _re2.Options opts
    cdef int error_code
    cdef int encoded = 0

    if isinstance(pattern, Pattern):
        return pattern

    cdef object original_pattern = pattern

    cdef str strflags = ''
    # Set the options given the flags above.
    if flags & _I:
        opts.set_case_sensitive(0);

    # The re.U flag is actually ignored since there
    # are no unicode dependent character classes yet...
    opts.set_encoding(_re2.EncodingUTF8)

    if not (flags & _X):
        opts.set_log_errors(0)

    if flags & _S:
        strflags += 's'
    if flags & _M:
        strflags += 'm'

    if strflags:
        pattern = '(?' + strflags + ')' + pattern

    # We use this function to get the proper length of the string.

    pattern = unicode_to_bytestring(pattern, &encoded)
    if pystring_to_bytestring(pattern, &string, &length) == -1:
        raise TypeError("first argument must be a string or compiled pattern")

    s = new _re2.StringPiece(string, length)

    cdef _re2.RE2 * re_pattern = new _re2.RE2(s[0], opts)
    if not re_pattern.ok():
        # Something went wrong with the compilation.
        del s
        error_msg = cpp_to_pystring(re_pattern.error())
        error_code = re_pattern.error_code()
        del re_pattern
        if current_notification == <int>FALLBACK_EXCEPTION:
            # Raise an exception regardless of the type of error.
            raise RegexError(error_msg)
        elif error_code != _re2.ErrorBadPerlOp and error_code != _re2.ErrorRepeatSize:
            # Raise an error because these will not be fixed by using the ``re`` module.
            raise RegexError(error_msg)
        elif current_notification == <int>FALLBACK_WARNING:
            warnings.warn("WARNING: Using re module. Reason: %s" % error_msg)
        return re.compile(pattern, flags)

    cdef Pattern pypattern = Pattern()
    pypattern.pattern = original_pattern
    pypattern.re_pattern = re_pattern
    pypattern.ngroups = re_pattern.NumberOfCapturingGroups()
    pypattern.encoded = <bint>encoded
    del s
    return pypattern

def search(pattern, string, int flags=0):
    """
    Scan through string looking for a match to the pattern, returning
    a match object or none if no match was found.
    """
    return compile(pattern, flags).search(string)

def match(pattern, string, int flags=0):
    """
    Try to apply the pattern at the start of the string, returning
    a match object, or None if no match was found.
    """
    return compile(pattern, flags).match(string)

def finditer(pattern, string, int flags=0):
    """
    Return an list of all non-overlapping matches in the
    string.  For each match, the iterator returns a match object.

    Empty matches are included in the result.
    """
    return compile(pattern, flags).finditer(string)

def findall(pattern, string, int flags=0):
    """
    Return an list of all non-overlapping matches in the
    string.  For each match, the iterator returns a match object.

    Empty matches are included in the result.
    """
    return compile(pattern, flags).findall(string)

def split(pattern, string, int maxsplit=0):
    """
    Split the source string by the occurrences of the pattern,
    returning a list containing the resulting substrings.
    """
    return compile(pattern).split(string, maxsplit)

def sub(pattern, repl, string, int count=0):
    """
    Return the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in string by the
    replacement repl.  repl can be either a string or a callable;
    if a string, backslash escapes in it are processed.  If it is
    a callable, it's passed the match object and must return
    a replacement string to be used.
    """
    return compile(pattern).sub(repl, string, count)

def subn(pattern, repl, string, int count=0):
    """
    Return a 2-tuple containing (new_string, number).
    new_string is the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in the source
    string by the replacement repl.  number is the number of
    substitutions that were made. repl can be either a string or a
    callable; if a string, backslash escapes in it are processed.
    If it is a callable, it's passed the match object and must
    return a replacement string to be used.
    """
    return compile(pattern).subn(repl, string, count)
