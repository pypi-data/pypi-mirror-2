List the content and structure of a Python project

Only tested on Microsoft Windows and Python 2.7

Docs and download: http://pypi.python.org/pypi/pyls
Source code: http://bitbucket.org/tartley/pyls


Usage
-----

::

    pyls [<dir1> [, <dir2>...] ]


Produces a listing of the python project in directly <dir>, or else in the
current directory if none given, in the following format::

    package
        subpackage
            module1.py
                ClassA
                ClassB
            module2.py
                ClassC
        module3.py
            ClassD


Known Issues
------------

Pyls works by importing every module it finds in the given directories, and
enumerating the classes defined by importing that module. If you are doing
anything cleverer than defining static classes in regular modules, then pyls
will probably barf on it.


Todo
----

* classes and functions exposed by a package (i.e. imported or defined in
  __init__.py) should show up in the output
* Test on Ubuntu
* Pester someone to test on a Mac for me
* Python 3
* accept command line directories specified as relative dirs (e.g. '..')
* List module-level functions too.
* Some way to differentiate classes from functions?
  e.g. func() or "def func()" and "class ClassA" ?)
* optional colored output?
* optionally list class methods?
* compact mode, that lists classes in a module on the same line?


Thanks
------

To Susan for putting up with my googly-eyed coding frenzies.

