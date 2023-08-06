Mooching files with Python
==========================

Sharing files on a local network made kinda easy.

**Share files with:**

  python -mooch -s filename filename filename dirname

Sharing a dirname shares all the files in that directory.

**Find files to mooch with:**

  python -mooch

**Grab a specific file with:**

  python -mooch filename

Use python -mooch to discover the other command-line arguments, such as
verbosity and port number controls.

Current limitations:

- you can't mooch and offer files on the same host
- the interface is a bit crap
- no support for auto-zipping files up
- actually, no compression at all
- and, you know, a bunch of stuff 'cos this is a toy thrown together in a
  few hours


Version History (in Brief)
--------------------------

- 1.0 is the initial release

----

Copyright (c) 2011 Richard Jones <http://mechanicalcat.net/richard>

See the source file for the license
