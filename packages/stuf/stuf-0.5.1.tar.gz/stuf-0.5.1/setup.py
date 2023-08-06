'''setup stuf'''

#Copyright (c) 2006-2011 L. C. Rees.  All rights reserved.
#Copyright (c) 2010 David Schoonover
#Copyright (c) 2009 Raymond Hettinger
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = []
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    install_requires.append('ordereddict')
    install_requires.append('unittest2')

setup(
    name='stuf',
    version='0.5.1',
    description='''stuf has attributes''',
    long_description='Collection of dictionaries that support access through '
    'dot notation. Includes defaultdict and OrderedDict equivalents and '
    'restricted and immutable dictionary types.',
    author='L. C. Rees',
    url='https://bitbucket.org/lcrees/stuf/',
    author_email='lcrees@gmail.com',
    license='MIT',
    packages=['stuf'],
    test_suite='stuf.test',
    zip_safe=False,
    keywords='dict attribute collection mapping dot notation access',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
