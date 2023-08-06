README
======

Sylli divides timit, strings, files and entire directories into 
syllables and provides other useful function for syllable analysis. 
Sylli was originally intended to be used with CLIPS (a corpus of spoken Italian)
and NLTK (see references), but can be used on any TIMIT file, string, and with
some changes languages and ASCII alphabet(default setting uses xSampa and 
syllabify Italian).

Please, for a complete, updated documentation visit: http://sylli.sourceforge.net

Install
*******

You can install Sylli by using the windows installer or the source.

To install using the installer just double-click the installer icon.

To install as a python module, you can either use python easy install

::

  $ easy_install sylli

Or install manually from the source code. To do so, follow these steps:

Install Python, version 2.3 or later - http://python.org/

Install wxPython - http://www.wxpython.org

Download the source code and unzip the content

::

  $ unzip sylli-x.x.x.zip

and install it with:

:: 

  $ cd Sylli
  $ python setup.py install

For more options use

::

  $ python setup.py --help

If you're using windows or planning to redistribute sylli as a windows installer or .exe read the Windows BUILD section below.

Usage
*****

To run sylli from the command line use

::

  $ sylli-command --help

The command 'sylli' is reserved for the GUI. 
This is the default install application in windows. If you installed from the source or on \*nix, you can launch it with

::

  $ sylli

or run it directly from the source code directory:

::

  $ python sylli/ui.py

For more information use the program help.
	
The latest alternative, is to import the module in python

::

  >>> import sylli


Windows BUILD
*************

Install Python, version 2.3 or later - http://python.org/

Install wxPython - http://www.wxpython.org

Install py2exe -
http://starship.python.net/crew/theller/py2exe/

Install the inno installer - http://www.jrsoftware.org/isdl.php

Download msvcr90.dll and copy it in the root syllable directory 

In a shell, go to the root syllable directory and run this command
python winsetup.py py2exe

copy sylli/htmldoc into sylli/build

Now compile inno.iss on inno

This will create an installer called sylli-{VERSION}.exe
The installer is completely self-contained and will work on any 
Windows machine, even without the above software having been 
installed.

References
**********
For license information read license.txt

For the changelog read changes.txt

For  advice,  bug  report, and everything feel free to mail
jacoponi@(at)gmail.com
