# -*- coding: utf-8 -*-

###
### $Release: $
### Copyright(c) 2009-2010 kuwata-lab.com all rights reserved.
### MIT License
###

import sys, os
if os.path.isfile("webext.so"):
    sys.path.append(".")
elif os.path.isfile("../webext.so"):
    sys.path.append("..")
import oktest
from oktest import ok, not_ok
import webext


def spec(detail):
    def deco(f):
        f.spec = detail
        return f
    return deco


class Webext_EscapeHtml_Test(object):

    @spec("escape html special characters")
    def test_to_escape_html_special_characters(self):
        s = '<foo> & "bar" & \'baz\''
        ret = webext.escape_html(s)
        ok (ret) == "&lt;foo&gt; &amp; &quot;bar&quot; &amp; 'baz'"
        #ok (ret) == "&lt;foo&gt; &amp; &quot;bar&quot; &amp; &#039;baz&#039;"

    @spec("if argument doesn't contain html special chars then return it")
    def test_that_same_object_is_returned_when_argument_is_str(self):
        s = "foo"
        ret = webext.escape_html(s)
        ok (ret) == s
        ok (ret).is_(s)
        ok (id(ret)) == id(s)

    @spec("if no argument then raises TypeError")
    def test_that_TypeError_is_raised_when_no_argument(self):
        def f():
            webext.escape_html()
        ok (f).raises(TypeError, "function takes exactly 1 argument (0 given)")

    @spec("if argument is None then return empty string")
    def test_to_return_empty_string_if_argument_is_None(self):
        ret = webext.escape_html(None)
        ok (ret) == ""

    @spec("if argument is None then return same object every time")
    def test_to_return_same_object_if_argument_is_None(self):
        ret  = webext.escape_html(None)
        ret2 = webext.escape_html(None)
        ok (ret).is_(ret2)
        ok (id(ret)) == id(ret2)

    @spec("if arg doesn't cntain html special chars then refcount should not be changed")
    def test_that_refcount_is_not_changed_when_arg_is_str_and_not_contain_htmlspecialchars(self):
        s = "foo"
        ret = webext.escape_html(s)
        refcnt = sys.getrefcount(ret)
        ret = webext.escape_html(s)
        ret = webext.escape_html(s)
        ret = webext.escape_html(s)
        ok (sys.getrefcount(ret)) == refcnt

    @spec("if arg is None then refcound of returned empty string is not changed")
    def test_that_refcnt_of_returned_empty_string_is_not_changed_when_arg_is_None(self):
        ret = webext.escape_html(None)
        refcnt = sys.getrefcount(ret)
        ret = webext.escape_html(None)
        ret = webext.escape_html(None)
        ret = webext.escape_html(None)
        ok (sys.getrefcount(ret)) == refcnt

    @spec("if arg is integer then converted into str")
    def test_that_integer_is_converted_into_str(self):
        ret = webext.escape_html(123)
        ok (ret).is_a(str)
        ok (ret) == "123"
        #
        ret = webext.escape_html(- 999)
        ok (ret).is_a(str)
        ok (ret) == "-999"

    @spec("if arg is float then converted into str")
    def test_that_float_is_converted_into_str(self):
        ret = webext.escape_html(3.14159)
        ok (ret).is_a(str)
        ok (ret) == "3.14159"
        #
        ret = webext.escape_html(- 0.1)
        ok (ret).is_a(str)
        ok (ret) == "-0.1"

    @spec("if arg is unicode then encoded into str")
    def test_that_unicode_is_converted_into_str(self):
        s = '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
        u = u'\u65e5\u672c\u8a9e'
        ok (u.encode('utf8')) == s
        ok (s.decode('utf8')) == u
        ret = webext.escape_html(u)
        ok (ret) == s;
        ret2 = webext.escape_html(u)
        ok (id(ret)) != id(ret2)


class Webext_ToStr_Test(object):

    @spec("if arg is str then returns same object")
    def test_that_same_object_is_returned_when_argument_is_str(self):
        s = "foo"
        ret = webext.to_str(s)
        ok (ret) == s
        ok (ret).is_(s)
        ok (id(ret)) == id(s)

    @spec("if no argment then raises TypeError")
    def test_that_TypeError_is_raised_when_no_argument(self):
        def f():
            webext.to_str()
        ok (f).raises(TypeError, "function takes exactly 1 argument (0 given)")

    @spec("if arg is None then returns empty string")
    def test_to_return_empty_string_if_argument_is_None(self):
        ret = webext.to_str(None)
        ok (ret) == ""

    @spec("if arg is None then returns same object everytime")
    def test_to_return_same_object_if_argument_is_None(self):
        ret  = webext.to_str(None)
        ret2 = webext.to_str(None)
        ok (ret).is_(ret2)
        ok (id(ret)) == id(ret2)

    @spec("if arg doesn't contain htmlspecialchars then refcount of arg should not be changed")
    def test_that_refcount_is_not_changed_when_arg_is_str_and_not_contain_htmlspecialchars(self):
        s = "foo"
        ret = webext.to_str(s)
        refcnt = sys.getrefcount(ret)
        ret = webext.to_str(s)
        ret = webext.to_str(s)
        ret = webext.to_str(s)
        ok (sys.getrefcount(ret)) == refcnt

    @spec("if arg is None then refcount of returned empty string should not be changed")
    def test_that_refcnt_of_returned_empty_string_is_not_changed_when_arg_is_None(self):
        ret = webext.to_str(None)
        refcnt = sys.getrefcount(ret)
        ret = webext.to_str(None)
        ret = webext.to_str(None)
        ret = webext.to_str(None)
        ok (sys.getrefcount(ret)) == refcnt

    @spec("if arg is integer then converts into str")
    def test_that_integer_is_converted_into_str(self):
        ret = webext.to_str(123)
        ok (ret).is_a(str)
        ok (ret) == "123"
        #
        ret = webext.to_str(- 999)
        ok (ret).is_a(str)
        ok (ret) == "-999"

    @spec("if arg is float then converts into str")
    def test_that_float_is_converted_into_str(self):
        ret = webext.to_str(3.14159)
        ok (ret).is_a(str)
        ok (ret) == "3.14159"
        #
        ret = webext.to_str(- 0.1)
        ok (ret).is_a(str)
        ok (ret) == "-0.1"

    @spec("if arg is unicode then encodes into str")
    def test_that_unicode_is_converted_into_str(self):
        s = '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
        u = u'\u65e5\u672c\u8a9e'
        ok (u.encode('utf8')) == s
        ok (s.decode('utf8')) == u
        ret = webext.to_str(u)
        ok (ret) == s;
        ret2 = webext.to_str(u)
        ok (id(ret)) != id(ret2);


class Webext_SetEncoding_Test(object):

    @spec("if encoding is set then to_str() and escape_html() are affected")
    def test_that_to_str_and_escape_html_are_affected_if_encoding_is_set(self):
        s = '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
        u = u'\u65e5\u672c\u8a9e'
        ok (u.encode('utf8')) == s
        ok (s.decode('utf8')) == u
        ok (webext.to_str(u)) == s
        ok (webext.escape_html(u)) == s
        #
        webext.set_encoding('euc-jp')
        try:
            ok (webext.to_str(u))      != s
            ok (webext.escape_html(u)) != s
        finally:
            webext.set_encoding('utf8')
        #
        webext.set_encoding('ascii')
        try:
            f = lambda: webext.to_str(u)
            ok (f).raises(UnicodeEncodeError, "'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)")
        finally:
            webext.set_encoding('utf8')


if __name__ == '__main__':
    oktest.run('Webext.*Test$')
