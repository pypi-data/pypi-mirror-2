History
=======

6.1.0 (2010-09-20)
------------------

* Changed version number to reflect readline version instead of Python version
* #4: Updated to build against readline 6.1 (patch-level 2)
* #2: Python 3 support
* Uses Python 2.x readline.c from release27-maint branch (r83672)
* Uses Python 3.x readline.c from r32a2 tag (r84541)
* Source code moved to GitHub
* Additional maintainer: Sridhar Ratnakumar

2.6.4 (2009-11-26)
------------------

* Added -fPIC to compiler flags to fix linking error on 64-bit Ubuntu
* Enabled all readline functionality specified in pyconfig.h macros
* Uses readline.c from Python svn trunk (r75725), which followed 2.6.4 release
* Patched readline.c to replace Py_XDECREF calls with the safer Py_CLEAR
* Fixed compilation error on Mac OS 10.4 with XCode older than version 2.4

2.6.1 (2009-11-18)
------------------

* Updated package to work with Mac OS 10.6 (Snow Leopard), which ships with 
  Python 2.6.1
* Uses readline.c from Python 2.6.1 release
* Backported "spurious trailing space" bugfix from Python svn trunk (see e.g. 
  https://bugs.launchpad.net/python/+bug/470824 for details on bug)
* Updated to build against readline 6.0 (patch-level 4)
* Now builds successfully on Linux (removed Mac-specific flags in this case),
  and still supports Mac OS 10.4 and 10.5

2.5.1 (2008-05-28)
------------------

* Updated package to work with Mac OS 10.5 (Leopard), which ships with Python 
  2.5.1
* Uses readline.c from Python 2.5.1 release
* Updated to build against readline 5.2 (patch-level 12)
* New maintainer: Ludwig Schwardt

2.4.2 (2005-12-26)
------------------

* Original package by Bob Ippolito, supporting Python 2.3 / 2.4 on Mac OS 10.3 
  (Panther) and 10.4 (Tiger)
* Builds against readline 5.1
