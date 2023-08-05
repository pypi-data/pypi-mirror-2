#!/usr/bin/env python

from distutils.core import setup

setup( name = 'wx_py',
       version = '0.9.8.3b',
       description = 'Py Suite including PyCrust and a revamped version, PySlices',
       author = "David Mashburn / Patrick O'Brian",
       author_email = 'david.n.mashburn@gmail.com',
       url = 'http://www.wxpython.org/py.php',
       scripts = ['postinstall.py'],
       packages = ['wx_py'],
     )
