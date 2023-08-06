===================
 Command Reference
===================

mktmpenv
========

Create a new virtualenv in the WORKON_HOME directory.

Syntax::

    mktmpenv [ENVNAME]

If no environment name is given, a temporary unique name is generated.

::

    $ mktmpenv
    Using real prefix '/Library/Frameworks/Python.framework/Versions/2.7'
    New python executable in 1e513ac6-616e-4d56-9aa5-9d0a3b305e20/bin/python
    Overwriting 1e513ac6-616e-4d56-9aa5-9d0a3b305e20/lib/python2.7/distutils/__init__.py 
    with new content
    Installing distribute...............................................
    ....................................................................
    .................................................................done.
    This is a temporary environment. It will be deleted when deactivated.
    (1e513ac6-616e-4d56-9aa5-9d0a3b305e20) $
