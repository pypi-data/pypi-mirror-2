------
rename
------

Renames files using regular expression matching. This enables elegant handling
of multiple renames using a single command.

Usage
=====

Basic syntax::

  rename [-t] "regex" "target"

Options
=======

-t, or --test
~~~~~~~~~~~~~
When used, the script will only fake renaming and verbosely state what it would
do. Use this if you're unsure of the effects your expression may cause.  

regex
~~~~~
Regular expression that matches source files which are to be renamed. Examples::

    "(\w+).caf"
    "IMG(\d\d\d\d\).[Jj][Pp][Ee]?[Gg]"
    "([0-9]{2})-([0-9]{2})-([12][0-9]{3}).log"

target
~~~~~~
Name of the target file with references to regular expression groups caught in
the source matches. References to groups are formed by a backslash character
followed by he group number. Groups are indexed from 1. The group number can be
contained within parentheses to disambiguate a reference followed by digits.
Examples::

    "\1.aiff"
    "\(1)1337.zip"
    "\3-\1-\2.log"

Installation
============

This script requires Python 2.4+ with the `argparse
<http://code.google.com/p/argparse/>`_ library. It can be used standalone or
installed using ``pip`` or ``easy_install``::

  pip install rename
  easy_install rename

Don't have either of these? You can always grab the latest source release from
the `PyPI website <http://pypi.python.org/pypi/rename#downloads>`_ or better yet
equip yourself with ``easy_install`` by downloading and running
`distribute_setup.py <http://python-distribute.org/distribute_setup.py>`_.

Security
========

1. The script will not let multiple files be renamed to a single name.

2. The script will not let existing files to be overwritten.

3. Both checks above are made for all matches before any renaming is performed.

Other remarks
=============

1. Regular expressions supported by the script must conform to the syntax
   handled by Python's `re <http://docs.python.org/library/re.html>`_ module.

2. The regular expression is global by default (e.g. writing ``"[0-9]"`` means
   ``"^[0-9]$``. This is to avoid accidental partial catches. If you want to
   match all files that start or end with a specific expression, add ``.*`` to
   the expression, e.g. ``".*\.mp3"`` will match all files that end with
   ``.mp3``.

3. Actual renaming of a single file is done by the `os.rename()
   <http://docs.python.org/library/os.html#os.rename>`_ function from Python's
   standard library. No additional atomicity is ensured, e.g. if a single rename
   fails halfway through, the filesystem is left in a state of partially
   complete renaming.

3. Due to differences in behaviour of different shells, the recommended form of
   execution is to put both arguments in quotation marks.

Possible future enhancements
============================

1. Automatic numbering with ``\(auto)`` target reference.

2. ``-p`` option to create intermediate directories for the target. One tiny
   problem is maintaining atomicity of the whole transaction.

3. ``-v except_regex`` option to constrain source matches to those that don't
   match ``except_regex``. This would enable easy handling of special cases.

4. ``-r`` option to make the source match recursive. Tricky to get right
   I guess, e.g. where to rename? Existing directory structure or new one?. Let
   the user decide? What's the default? Etc. etc.

5. ``-s`` option to enable a "translate" mode to replace certain substrings with
   others. Proposed syntax::
    
    rename -s "substring_from" "substring_to" "file_match_regex"
    
   Example (translating underscores to spaces)::

    rename -s "_" " " ".*\.txt" 

   This would be more-less compatible with behaviour of the existing ``rename``
   tool from the ``util-linux-ng`` package. One obvious difference would be that
   the file mask doesn't use wildcards but regular expressions.

6. ``-l`` option to enable translating all letters to lowercase. ``-U`` option
   to translate letters to uppercase.

BFD: BIG FRIENDLY DISCLAIMER
============================

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

**DON'T PANIC**. This code has been successfully used by its author. However, be
especially wary under these conditions:

1. Renaming between filesystems.

2. Renaming under case-insensitive filesystems.

3. Renaming within very long paths.

4. Renaming volatile state (e.g. rotating logs).

And if you do lose any data, it's your fault. Have a nice day!

Authors
=======

Script glued together by `Łukasz Langa <mailto:lukasz@langa.pl>`_.
