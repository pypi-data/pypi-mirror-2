###
### $Release: 0.0.1 $
### $Copyright: Copyright(c) 2009-2010 kuwata-lab.com all rights reserved. $
### $License: MIT License $
###
### ex.
###   $ python setup.py build
###   $ ls -F build/
###   lib.macosx-10.6-i386-2.5/
###   $ ls -F build/*/
###   webext.so*
###   $ ln -s build/*/webext.so .
###   $ python
###   >>> import webext
###   >>> webext.escape_html('<b>AAA&BBB</b>')
###   &lt;b&gt;AAA&amp;BBB&lt;/b&gt;
###   >>> s = webext.escape_html(None)
###   >>> repr(s)
###   ''
###

import sys, re, os
arg1 = len(sys.argv) > 1 and sys.argv[1] or None
if arg1 == 'egg_info':
    from ez_setup import use_setuptools
    use_setuptools()
if arg1 == 'bdist_egg':
    from setuptools import setup, Extension
else:
    from distutils.core import setup, Extension

version = '$Release: 0.0.1 $'.split(' ')[1]

setup(
    name         = 'Webext',
    version      = version,
    description  = 'C extension module for escape_html()',
    url          = 'http://pypi.python.org/Webext/',
    author       = 'makoto kuwata',
    author_email = 'kwa@kuwata-lab.com',
    ext_modules  = [ Extension('webext', sources=['webext.c']) ],
    long_description = r"""Webext is a library to provide very fast 'escape_html()' function.
It is implemented as C extension and it runs much faster than pure Python code
such as 'cgi.escape()'.


Installation
------------

::

   $ tar xzf Webext-0.0.1.tar.gz
   $ cd Webext-0.0.1
   $ sudo python setup.py install


Functions
---------

Webext provides following functions:

* webext.escape_html()

  - escapes HTML special characters (< > & ").
  - converts unicode into str with 'utf8' encoding.
  - converts None into empty string (= '').

* webext.escape()

  - alias to webext.escape_html()

* webext.to_str()

  - converts argument into str (same as str())
  - converts unicode into str with 'utf8' encoding.
  - converts None into empty string (= '').

* webext.get_encoding()

  - returns default encoding for escape_html() and to_str()
  - default value is 'utf8'

* webext.set_encoding(arg)

  - sets default encoding for escape_html() and to_str()


Example
-------

::

   ### import escape_html() and to_str()
   >>> from webext import escape_html, to_str

   ### escape_html() escapes html special characters
   >>> escape_html('< > & "')
   '&lt; &gt; &amp; &quot;'

   ### to_str() and escape_html() convert unicode into str with 'utf8' encoding
   >>> to_str(u'\u65e5\u672c\u8a9e')
   '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
   >>> escape_html(u'\u65e5\u672c\u8a9e')
   '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'

   ### to_str() and escape_html() convert None into empty string
   ### (this is more desirable than str() for web application)
   >>> to_str(None)
   ''
   >>> escape_html(None)
   ''


Using with Tenjin
-----------------

`Tenjin <http://www.kuwata-lab.com/tenjin/>`_ is a very fast template engine
implemented in pure Python. You can make Tenjin much faster by using Webext.

::

    import tenjin
    from tenjin.helpers import *
    from webext import to_str, escape    # use webext's to_str() and escape() instead of tenjin's
    engine = tenjin.Engine()
    context = { 'items': ['<AAA>', 'B&B', '"CCC"'] }
    print engine.render('example.pyhtml', context)


Tenjin's benchmark now supports Webext. The following is an example of
benchmark result on Mac OS X 10.6, Intel Core Duo 2GHz, Tenjin 0.9.0.
This shows that Webext boosts Tenjin especially html escaping.

::

    ## without html escaping
    $ python bench.py -n 10000 tenjin tenjin-
    webext
    import tenjin ... done. (0.001740 sec)
    import webext ... done. (0.000466 sec)
    *** loading context data (file=bench_context.py)...
    *** start benchmark
    *** ntimes=10000
                                        utime     stime     total      real
    tenjin                             3.8100    0.0400    3.8500    3.8584
    tenjin-webext                      2.5000    0.0300    2.5300    2.5367
    
    ## with html escaping
    $ python bench.py -e -n 10000 tenjin tenj
    in-webext
    import tenjin ... done. (0.001580 sec)
    import webext ... done. (0.000459 sec)
    *** loading context data (file=bench_context.py)...
    *** start benchmark
    *** ntimes=10000
                                        utime     stime     total      real
    tenjin                             7.2100    0.0500    7.2600    7.2935
    tenjin-webext                      2.9800    0.0400    3.0200    3.0476
""",
    license      = 'MIT License',
    platforms    = 'any',
    download_url = 'http://pypi.python.org/packages/source/W/Webext/Webext-0.0.1.tar.gz',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        #'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        #'Programming Language :: Python :: 2.3',
        #'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        ],
    #py_modules  = ['webext'],
    #package_dir = {'': 'lib'},
    #scripts     = [],
    #zip_safe    = False,
)
