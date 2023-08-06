#!/usr/bin/env python

from distutils.core import setup
from distutils.sysconfig import get_python_lib

setup(name='pyspread',
      version='0.1.2',
      description='A spreadsheet that accepts a pure python expression in each cell.',
      license='GPL v3 :: GNU General Public License',
      classifiers=[ 'Development Status :: 4 - Beta',
                    'Environment :: MacOS X',
                    'Environment :: Win32 (MS Windows)',
                    'Environment :: X11 Applications :: GTK',
                    'Intended Audience :: End Users/Desktop',
                    'License :: OSI Approved :: GNU General Public License (GPL)',
                    'Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python :: 2.4',
                    'Programming Language :: Python :: 2.5',
                    'Programming Language :: Python :: 2.6',
                    'Topic :: Office/Business :: Financial :: Spreadsheet',
      ],
      author='Martin Manns',
      author_email='mmanns@gmx.net',
      url='http://pyspread.sourceforge.net',
      requires=['numpy (>=1.1)', 'wx (>=2.8.10)'],
      scripts=['_pyspread/pyspread'],
      packages=['_pyspread'],
      package_data={'_pyspread': ['icons/*.png', 'icons/actions/*.png', 
                                  'icons/toggles/*.png', 'icons/toggles/*.xpm',
                                  'examples/*', 'doc/*.html', 
                                  'doc/images/*.png', 'README', 'COPYING']},
)
