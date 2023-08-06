------
rename
------

Renames files using regular expression matching. This enables elegant handling
of multiple renames using a single command.

Usage
=====

Basic syntax::

  rename [-i] [-l] [-t] [-u] [-v "except_regex"] "regex" "target"

Options
=======

regex
~~~~~
Regular expression that matches source files which are to be renamed. Examples::

    "(\w+).caf"
    "IMG(\d\d\d\d\).[Jj][Pp][Ee]?[Gg]"
    "([0-9]{2})-([0-9]{2})-([12][0-9]{3}).log"

The regular expression is **global** by default (e.g. writing ``"[0-9]"`` means
``"^[0-9]$``. This is to avoid accidental partial catches. If you want to match
all files that start or end with a specific expression, add ``.*`` to the
expression, e.g. ``".*\.mp3"`` will match all files that end with ``.mp3``.
While that may seem a bit redundant, it's on par with *"explicit is better than
inplicit"* (see `The Zen of Python
<http://www.python.org/dev/peps/pep-0020/>`_). See also: ``-i``.

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

-i, or --case-insensitive
~~~~~~~~~~~~~~~~~~~~~~~~~
When used, regexes work in a case-insensitive manner, e.g. ``"lib"`` will behave
like ``"[Ll][Ii][Bb]"``. Group references still hold the original case.

-l, or --lower
~~~~~~~~~~~~~~
When used, renamed filenames are transformed to lower-case. This does not affect
the source regex used (i.e. unless ``-i`` is used, it still matches in
a case-sensitive manner). See also: ``-U``.

-t, or --test
~~~~~~~~~~~~~
When used, the script will only fake renaming and verbosely state what it would
do. Use this if you're unsure of the effects your expression may cause.  

-U, or --upper
~~~~~~~~~~~~~~
When used, renamed filenames are transformed to upper-case. This does not affect
the source regex used (i.e. unless ``-i`` is used, it still matches in
a case-sensitive manner). See also: ``-l``.

-v "except_regex", or --except "except_regex"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When used, any filename matched by the original source regex will be also
matched against the ``except_regex``. In case there is a match, the filename is
skipped. In other words, filenames that match ``except_regex`` will **not** be
renamed.

The regular expression is **local** (e.g. writing ``"[0-3]"`` means "number
0-3 anywhere in the filename). This is to make the tool err on the side of
caution by protecting from renaming too many files by accident when the user
forgets to add dot-asterisk to ``-v``. If you want to only match whole
filenames, use the canonical global form (e.g. ``"^filename$"``).
See also: ``-i``.

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

2. Actual renaming of a single file is done by the `os.rename()
   <http://docs.python.org/library/os.html#os.rename>`_ function from Python's
   standard library. No additional atomicity is ensured, e.g. if a single rename
   fails halfway through, the filesystem is left in a state of partially
   complete renaming.

3. Due to differences in behaviour of different shells, the recommended form of
   execution is to put both arguments in quotation marks.

Possible future enhancements
============================

1. Automatic numbering with ``\(auto)`` target reference.

2. ``-s`` option to enable a "translate" mode to replace certain substrings with
   others. Proposed syntax::
    
    rename -s "substring_from" "substring_to" "file_match_regex"
    
   Example (translating underscores to spaces)::

    rename -s "_" " " ".*\.txt" 

   This would be more-less compatible with behaviour of the existing ``rename``
   tool from the ``util-linux-ng`` package. One obvious difference would be that
   the file mask doesn't use wildcards but regular expressions.

3. ``-p`` option to create intermediate directories for the target. One tiny
   problem is maintaining atomicity of the whole transaction.

4. ``-r`` option to make the source match recursive. Tricky to get right
   I guess, e.g. where to rename? Existing directory structure or new one?. Let
   the user decide? What's the default? Etc. etc.

BFD: BIG FRIENDLY DISCLAIMER
============================

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

**DON'T PANIC**. This code has been successfully used by its author and
contains tests. However, be especially wary under these conditions:

1. Renaming between filesystems.

2. Renaming under case-insensitive filesystems.

3. Renaming within very long paths.

4. Renaming volatile state (e.g. rotating logs).

And if you do lose any data, it's your fault. Have a nice day!

Authors
=======

Script glued together by `Łukasz Langa <mailto:lukasz@langa.pl>`_.
