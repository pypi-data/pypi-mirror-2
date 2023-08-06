Petapass
--------

Petapass makes better passwords using stateless hashes.

The traditional approach to password management is to store passwords in an encrypted file (various password managers use this approach). Petapass instead implements a 'stateless' password management scheme (all state resides in your head). It uses a master password and per-login descriptive token to generate unique 10-character passwords. The token is merely something you will remember when you need to log in.

See this `blog post <http://blog.wearpants.org/introducing-petapass>`_ for more information.

Usage
=====
Petapass has a single script named ``petapass`` with various subcommands. It features two modes of operation: single and daemon. Enter your master password and a token - the generated password will be copied to the clipboard.

Single
******
Single mode uses a simple terminal UI. It allows you to generate a single password. Run ``petapass one`` in a shell.

Daemon
******
Daemon mode starts a long running-process using a hidden GTK window. The master password will be remembered for a user-configurable timeout. Upon activation, the window is displayed and a token can be entered ::

    petapass daemon --help
    usage: petapass daemon [-h] [--timeout TIMEOUT]
    
    optional arguments:
      -h, --help         show this help message and exit
      --timeout TIMEOUT  how long to remember the master password, in minutes.
                         Default: 15

Show the window using ``petapass show``. You may want to bind this to a hotkey in your window manager. The password entry box is reasonably intelligent and may be controlled using only tab/enter (it works as you would hope). Click the ``Cancel`` or hit the escape key to dismiss the window. 

To clear the master password, click the ``Forget`` button or run ``petapass forget``. You may want to add this command to your `power management sleep hooks <http://manpages.ubuntu.com/manpages/jaunty/man8/pm-action.8.html#contenttoc4>`_ so that the master password is cleared when you suspend or hibernate your laptop.

Quit the daemon by pressing ``Control-q`` when the window is visible, or by running ``petapass kill``.

Platform
========
Single mode works on Linux and OS X. Linux users need `xclip <http://sourceforge.net/projects/xclip/>`_, available in most distros repositories. Daemon mode requires `pygtk <http://www.pygtk.org/>`_. Petapass works on Python 2.7, or Python 2.6 with `argparse <http://pypi.python.org/pypi/argparse>`_.

Bugs
====
The window doesn't always raise to the top & receive focus when shown. Adding Windows support should be trivial, but the author does not care to do so himself. Patches welcome. More `bugs here <http://hg.wearpants.org/petapass/issues/>`_.
