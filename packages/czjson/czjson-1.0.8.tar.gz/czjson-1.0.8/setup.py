#!/usr/bin/python

from distutils.core import setup, Extension

__version__ = "1.0.8"

macros = [('MODULE_VERSION', '"%s"' % __version__)]

setup(name         = "czjson",
      version      = __version__,
      author       = "zuroc",
      author_email = "zsp007@gmail.com",
      #url          = "http://ag-projects.com/",
      #download_url = "http://cheeseshop.python.org/pypi/python-cjson/%s" % __version__,
      description  = "Fast JSON encoder/decoder for Python(fix bug for python-cjson)",
      long_description = open('README').read(),
      license      = "LGPL",
      platforms    = ["Platform Independent"],
      classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
      ],
      ext_modules  = [
        Extension(name='czjson', sources=['cjson.c'], define_macros=macros)
      ]
)
