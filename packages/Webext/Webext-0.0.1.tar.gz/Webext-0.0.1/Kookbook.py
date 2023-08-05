# -*- coding: utf-8 -*-

from __future__ import with_statement

import sys, os, re

release   = prop('release', '0.0.1')
copyright = 'Copyright(c) 2009-2010 kuwata-lab.com all rights reserved.'
license   = 'MIT License'
kook_default_product = 'test'

text_files = ("README.txt", "CHANGES.txt", "Kookbook.py", "MANIFEST.in",
              "MIT-LICENSE", "ez_setup.py", "setup.py")

@recipe
def test(c):
    system("python test/test_*.py")

@recipe
def build(c):
    "build *.c"
    system("python setup.py build")

@recipe
def clean(c):
    system("python setup.py clean")
    rm_rf('dist', 'build', 'README.html', 'style.css')


curr_path = os.getcwd()
oktest_dir = re.sub(r'/webext/.*', '/oktest/', curr_path)
oktest_py = oktest_dir + "python/lib/oktest.py"

if os.path.isfile(oktest_py):
    @recipe("test/oktest.py", [oktest_py])
    def file_oktest_py(c):
        "copy oktest.py into 'test'"
        cp(c.ingred, c.product)


@recipe
@ingreds('dist/Webext-%s.tar.gz' % release)
def package(c):
    "create dist/Webext-x.x.x.tar.gz"
    with chdir("dist"):
        system(c%"tar xzf Webext-$(release).tar.gz")

@recipe
@product('dist/Webext-%s.tar.gz' % release)
@ingreds('edit')
def file_Webext_tar_gz(c):
    tmpdir = "dist/tmp"
    rm_rf(tmpdir)
    mkdir_p(tmpdir)
    cp(text_files, tmpdir)
    cp("webext.c", tmpdir)
    mkdir(c%"$(tmpdir)/test")
    cp("test/*.py", c%"$(tmpdir)/test")
    #
    def f(s):
        #s = re.sub(r'\$Release:.*?\$', '$Release: %s $' % release, s)
        s = re.sub(r'\$Release\$', release, s)
        #s = re.sub(r'\$Copyright:.*?\$', '$Copyright: %s $' % copyright, s)
        s = re.sub(r'\$Copyright\$', copyright, s)
        #s = re.sub(r'\$License:.*?\$', '$License: %s $' % license, s)
        s = re.sub(r'\$License\$', license, s)
        return s
    edit("%s/**/*" % tmpdir, by=f)
    def f(s):
        s = re.sub(r'X\.X\.X', release, s)
        return s
    edit("%s/README.txt" % tmpdir, by=f)
    #
    with chdir(tmpdir):
        system("python setup.py build")
        system("python setup.py sdist")
    #
    mv(c%"$(tmpdir)/dist/Webext-$(release).tar.gz", "dist")
    rm_rf(tmpdir)


@recipe
def task_edit(c, *args, **kwargs):
    if args:
        files = args
    else:
        files = [ x for x in text_files if x != 'Kookbook.py' ] + ['webext.c']
    def f(s):
        s = re.sub(r'\$Release:.*?\$',   '$Release: %s $'   % release,   s)
        s = re.sub(r'\$Copyright:.*?\$', '$Copyright: %s $' % copyright, s)
        s = re.sub(r'\$License:.*?\$',   '$License: %s $'   % license,   s)
        s = re.sub(r'Webext-\d\.\d\.\d', 'Webext-%s'        % release,   s)
        return s
    edit(files, by=f)


@recipe
@product('*.html')
@ingreds('$(1).txt')
def file_html(c):
    if not os.path.exists('style.css'):
        #touch('style.css')
        open('style.css', 'w').close()
    rst_opts = '-i utf-8 -o utf-8 -l ja --stylesheet=style.css --link-stylesheet --no-xml-declaration --no-generator'
    system(c%"rst2html.py $(rst_opts) $(ingred) > $(product)")

@recipe
@ingreds('README.html')
def task_html(c):
    pass
