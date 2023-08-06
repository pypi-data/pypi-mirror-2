xmlcmd
~~~~~~

xmlcmd is a proof of concept experiment in augmenting standard POSIX commands
with superpowers, such as outputting xml.

Sadly it is more sleight of hand than any real magic.

To begin with, a directory which is first on the ``PATH`` must be created
(e.g. ~/bin). This should not be on the path which ``whereis`` uses, so if
things go wrong you can always do ``$(whereis cmd)`` to execute affected
commands.

The idea is to put symlinks to xmlcmd (which is created in the normal ``python
setup.py install`` installation) into this directory for a number of commands.
When these commands are run with an --xml option, the _{cmd} module will be
imported from the xmlcmd package and the ``main()`` function run with two
arguments: the original list of command line arguments (typically corresponding
to sys.argv) minus the ``--xml``, and the full path to the 'original' file
which would have been run if the ``--xml`` option had not been specified.

This is similar to the way ``busybox`` works to implement a whole range of UNIX commands from a single binary, by using argv[0] to determine the required
action.  This allows the relevant logic to be factored out into a single place.

::

    ben$ sudo pip install xmlcmd
    ...
    ben$ ln -s $(which xmlcmd) ~/bin/ls
    ben$ ls --xml
    <an XMLish representation of a file listing...>

Plans:

1. Add a few more commands (currently only supports ls and ps)
2. Put a bunch of actually helpful XML output things into the xmlcmd package to
simplify creation of additional command helpers
3. A more useful ``xpath`` command than the perl program of that name on my
OS X and Ubuntu installs

Ben Bass 2011
