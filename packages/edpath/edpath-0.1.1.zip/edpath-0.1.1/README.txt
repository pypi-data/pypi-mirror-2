MS Windows command-line script to view and edit PATH-like environment variables.

Download and docs:
    http://pypi.python.org/pypi/edpath
Development:
    http://code.google.com/p/edpath

Description
-----------

Running edpath displays entries from the PATH (or other named environment
variable), with ';' separators replaced by newlines, so that each entry is on
its own line. Running with -e displays this in $EDITOR, and saved changes are
written back to the registry, where they will be picked up by all new
processes.

Run with -h for description and usage.


Requirements
------------

MS Windows only. Only tested on Windows XP.

Requires Python 2.7.

Requires that pywin32 is installed, from:
http://sourceforge.net/projects/pywin32/files/


Status and Known Problems
-------------------------

Feature complete. No known issues.

If you have comments or it doesn't work for you or you find bugs, I'd love to
hear about it. -tartley@tartley.com


Todo
----

  * invert the sense of options.machine to get rid of all those nots
  * support more versions of Python
  * produce a standalone py2exe version
  * store backups of old PATH values in case user trashes their PATH?
  * make Linux-friendly. Presumably we can only display the output there, not
    persist it.


Thanks
------

Thanks to Tim Golden for his marvellous descriptions and code snippets showing
how to read & modify environment variables in the Windows registry.

Changes
-------

0.1.0 Initial release. Feature complete.

