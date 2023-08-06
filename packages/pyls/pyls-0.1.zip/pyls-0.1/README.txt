List the content and structure of a Python project

Only tested on Microsoft Windows and Python 2.7

Usage
-----

    pyls

Produces a listing of the python project in directly <dir>, or else in the
current directory if none given, in the following format:

    package
        subpackage
            module1
                ClassA
                ClassB
            module2
                ClassC
        module3
            ClassD
    etc.


Known Issues
------------

Pyls works by recursively walking subdirectories, importing every module we
find, and enumerating the clases defined by importing that module. If you are
doing anything clever or dynamic, pyls almost certainly won't understand it.


Todo
----

* accept command line directories specified as relative dirs (e.g. '..')
* List module-level functions too
* optionally list class methods too

Thanks
------

