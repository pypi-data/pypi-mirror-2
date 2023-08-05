This is a fork of Ulrich Petri's branch
=======================================
It uses os.path.realpath() to allow for opening the file in the same project
window in the cases where the edited file is accessed through a symbolic
link.

Matthew Schinckel <matt@schinckel.net>
2009-11-20

This is a fork of PdbTextMateSupport 0.3
========================================
It tries to invoke the applescript call through py-appscript_ which is much 
faster than the os.system() call to 'osascript'.

  .. _py-appscript: http://appscript.sourceforge.net/py-appscript/index.html

Ulrich Petri, mail (at) ulo dot pe
2009-04-11

PdbTextMateSupport v0.3
=======================

View your source code in TextMate while debugging with pdb
----------------------------------------------------------

This module is used to hook up pdb_, the python debugger, with TextMate_, an
advanced text and programming editor for Mac OS, enabling it to display the
debugged source code during a pdb_ session.

  .. _pdb: http://docs.python.org/lib/module-pdb.html
  .. _TextMate: http://macromates.com/

After downloading and unpacking the package, you should install the helper
module using::

    $ python setup.py install

Next you need to hook up pdb_ with this module by add the following to your
``.pdbrc``::

    from PdbTextMateSupport import preloop, precmd
    pdb.Pdb.preloop = preloop
    pdb.Pdb.precmd = precmd

The easiest way to do this is to use the provided script::

    $ pdbtmsupport enable

Alternatively you can also do it manually.  The ``.pdbrc`` is located in your
home folder and possibly needs to be created first.  You may also use the
supplied sample configuration file for pdb_ to enable the hook like::

    $ cp pdbrc.sample ~/.pdbrc

Afterwards TextMate_ should get started automatically whenever you enter a
debug session.  The current source line will be displayed simultaneously while
stepping through the code.  However, having the cursor moved automatically
within that source file is not always very obvious, so you might want to use
the "Highlight current line" feature, which can be enabled in the "General"
tab in TextMate's preferences.


Andreas Zeidler, az@zitc.de,
2007/02/18
