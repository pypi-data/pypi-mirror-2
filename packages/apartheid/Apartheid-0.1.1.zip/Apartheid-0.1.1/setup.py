"""
Apartheid
-----

Apartheid is a simple parser for Python.

License: MIT

How to...?
````````````

-----
Print all #include statements in a C/C++ file?
-----

    from apartheid import parse

    elems = parse('#include "foo.h"\nint val = 42;\n', 'c')
    for elem in elems:
        if elem.name == 'include':
            print str(elem)

-----
Setup?
-----

    $ easy_install apartheid

Links
`````

* `website <http://github.com/shawnpresser/apartheid/>`_

"""
import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

def run_tests():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    from apartheid_tests import suite
    return suite()

setup(
    name='Apartheid',
    version='0.1.1',
    url='http://github.com/shawnpresser/apartheid/',
    license='MIT',
    author='Shawn Presser',
    author_email='shawnpresser@gmail.com',
    description='A simple parser (to parse a C file for example)',
    keywords='lexer tokenize tokenization parse parser text',
    py_modules=['distribute_setup','apartheid'],
    platforms='any',
    install_requires=[
        'Plexer>=0.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='__main__.run_tests'
)



