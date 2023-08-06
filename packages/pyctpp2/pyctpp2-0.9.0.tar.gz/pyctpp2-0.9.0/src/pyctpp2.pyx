# encoding: utf-8
# Copyright (c) 2011 Volvox Development Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: Konstantin Lepa <konstantin.lepa@gmail.com>

from cengine cimport CEngine
from ctemplate cimport CTemplate
from cdt cimport CDT, CDTAssign
cimport error_type as err
from libc.stdint cimport uint32_t, int64_t
from string cimport string, const_char_ptr
from cpython cimport exc
from cython.operator cimport dereference as deref
from libcpp.vector cimport vector

import os

include "pyversion.pxi"
include "version.py"

IF PYTHON_VERSION >= 3:
    ctypedef str StringType
    cdef str empty_string = str()
    cdef str string_type_to_str():
        return str(str)
    cdef bytes str_to_bytes(StringType s):
        return s.encode('UTF-8')
    cdef StringType c_str_to_str(const_char_ptr c):
        return c.decode('UTF-8', 'strict')
    cdef bint isunicode(s):
        return isinstance(s, str)
    xrange = range
ELSE:
    from cpython cimport unicode

    ctypedef bytes StringType
    cdef bytes empty_string = bytes()
    cdef bytes string_type_to_str():
        return str(unicode)
    cdef bytes str_to_bytes(StringType s):
        return s
    cdef StringType c_str_to_str(const_char_ptr c):
        return c
    cdef bint isunicode(s):
        return isinstance(s, unicode)

cdef raise_error(err.ErrorType etype, string message_):
    cdef const_char_ptr c_str = message_.c_str()
    cdef StringType message = c_str_to_str(c_str)
    if etype == err.kNoErrorType:
        raise Exception(message)
    elif etype == err.kNoMemoryErrorType:
        exc.PyErr_NoMemory()
    elif etype == err.kSystemErrorType:
        raise SystemError(message)
    elif etype == err.kIOErrorType:
        raise IOError(message)

cdef class Template

cdef class Engine:
    """CTPP2 Engine class."""
    cdef CEngine *thisptr
    cdef frozenset include_dirs

    property path:
        """Template path."""

        def __get__(self):
            return self.include_dirs

        def __set__(self, value):
            cdef vector[string] dirs
            cdef char *c_str
            cdef string s_str
            cdef bytes bt_str

            self.include_dirs = frozenset(value)
            for v in self.include_dirs:
                if isunicode(v):
                    bt_str = str_to_bytes(v)
                elif isinstance(v, bytes):
                    bt_str = v
                else:
                    raise ValueError("It has invalid value type")
                c_str = bt_str
                s_str.clear()
                s_str.append(c_str)
                dirs.push_back(s_str)
            self.thisptr.set_include_dirs(dirs)

        def __del__(self):
            cdef vector[string] dirs
            self.include_dirs = frozenset()
            self.thisptr.set_include_dirs(dirs)


    def __cinit__(self):
        self.thisptr = new CEngine()

    def __dealloc__(self):
        del self.thisptr

    def __init__(self,
            uint32_t arg_stack_size=10240,
            uint32_t code_stack_size=10240,
            uint32_t steps_limit=1048576,
            uint32_t max_func=1024):
        """x.__init__(arg_stack_size=10240,
                      code_stack_size=10240,
                      steps_limit=1048576,
                      max_func=1024) --

        'arg_stack_size'  - Max. size of stack of arguments
        'code_stack_size' - Max. stack size
        'max_func'        - Max. number of functions in CTPP standard library

        Normally you should now change these parameters, to explanation please
        refer to CTPP library documentation.

        'steps_limit' - template execution limit (in steps). Default value
        is 1 048 576 (1024*1024). You can limit template execution time by
        specifying this parameter [default: 1048576].

        Note, if execution limit is reached, template engine generates error
        and you should use try/except to catch it.
        """

        cdef string err_msg
        if not self.thisptr.Init(arg_stack_size, code_stack_size,
                steps_limit, max_func):
            err_msg = self.thisptr.last_error_message()
            raise_error(self.thisptr.last_error_type(), err_msg);

    def load_bytecode(self, const_char_ptr filename):
        """x.load_bytecode(filename) -- load precompiled template from
        specified file.

        ATTENTION: you should specify FULL path to precompiled file,
        CTPP DOES NOT uses include_dirs to search bytecode!
        """
        cdef CTemplate *tmpl
        cdef string err_msg
        if not self.thisptr.LoadBytecode(filename, &tmpl):
            err_msg = self.thisptr.last_error_message()
            raise_error(self.thisptr.last_error_type(), err_msg);
        return self.create_template(tmpl)

    def parse(self, const_char_ptr filename, str encoding="UTF-8"):
        """x.parse(filename, encoding="UTF-8") -- compile source code of
        template to CTPP bytecode.
        """

        cdef CTemplate *tmpl
        cdef string err_msg
        if not self.thisptr.Parse(filename, &tmpl):
            err_msg = self.thisptr.last_error_message()
            raise_error(self.thisptr.last_error_type(), err_msg);
        return self.create_template(tmpl, encoding)

    def parse_text(self, const_char_ptr text):
        """x.parse_text(text) -- compile text of template to CTPP bytecode."""
        cdef CTemplate *tmpl
        cdef string err_msg
        if not self.thisptr.ParseText(text, &tmpl):
            err_msg = self.thisptr.last_error_message()
            raise_error(self.thisptr.last_error_type(), err_msg);
        return self.create_template(tmpl)

    def add_user_function(self, const_char_ptr libname, const_char_ptr instance):
        """x.add_user_function(libname, instance) -- add user-defined function
        from external storage.

        If you have a shared library wich contains compiled user-defined
        functions, you may load it by calling method add_user_function().
        Please refer to documentation to explain, how you can write
        user-defined CTPP functions in C++.
        """

        cdef string err_msg
        if not self.thisptr.AddUserFunction(libname, instance):
            err_msg = self.thisptr.last_error_message()
            raise_error(self.thisptr.last_error_type(), err_msg);

    cdef Template create_template(self, CTemplate *template, str encoding="UTF-8"):
        cdef Template tmpl
        tmpl = Template.__new__(Template)
        tmpl.thisptr = template
        tmpl.engine = self
        tmpl.encoding = encoding
        return tmpl


cdef class Template:
    """CTPP2 Template class."""
    cdef CTemplate *thisptr
    cdef Engine engine
    cdef str encoding

    def __cinit__(self):
        self.thisptr = NULL
        self.engine = None

    def __dealloc__(self):
        del self.thisptr

    def __init__(self):
        raise TypeError("This class cannot be instantiated from Python")

    def save_bytecode(self, const_char_ptr filename):
        """x.save_bytecode(filename) -- save precompiled template to
        specified file.
        """

        cdef string err_msg
        if not self.thisptr.SaveBytecode(filename):
            err_msg = self.thisptr.last_error_message()
            raise_error(self.thisptr.last_error_type(), err_msg);

    def render(self, **kwargs):
        """x.render(**kwargs) -- render with variables."""
        cdef CDT cdt
        cdef int idx
        traverse(kwargs, &cdt)

        cdef string err_msg
        cdef string result
        if not self.thisptr.Render(cdt, &result):
            err_msg = self.thisptr.last_error_message()
            raise_error(self.thisptr.last_error_type(), err_msg);

        cdef const_char_ptr c_str = result.c_str()
        return c_str.decode(self.encoding, 'strict')


cdef traverse(obj, CDT *cdt, CDT *root_cdt=NULL, StringType prev_key=empty_string):
    cdef int idx
    cdef CDT tmp
    cdef char *c_str
    cdef bytes bt_str
    cdef StringType key

    if isinstance(obj, (int, bool)):
        CDTAssign(cdt, <int64_t>obj)
    elif isinstance(obj, float):
        CDTAssign(cdt, <double>obj)
    elif isunicode(obj):
        bt_str = obj.encode('UTF-8')
        c_str = bt_str
        CDTAssign(cdt, c_str)
    elif isinstance(obj, bytes):
        bt_str = obj
        c_str = bt_str
        CDTAssign(cdt, c_str)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            tmp = CDT()
            if prev_key:
                key = prev_key + '.' + key

            traverse(value, &tmp, cdt, key)
            IF PYTHON_VERSION >= 3:
                c_str = key.encode('UTF-8')
            ELSE:
                c_str = key

            if root_cdt:
                (deref(root_cdt))[c_str] = tmp
            else:
                (deref(cdt))[c_str] = tmp
    elif isinstance(obj, (tuple, list)):
        for idx in xrange(len(obj)):
            tmp = CDT()
            traverse(obj[idx], &tmp)
            (deref(cdt))[idx] = tmp

    cdef const_char_ptr dump_c
    cdef bytes dump_b
    cdef string dump_s

