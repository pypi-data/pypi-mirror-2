
========
noncrawl
========

noncrawl is a crawler that saves only links. It crawls the web but
does not attempt to do everything. Instead, its only purpose is to
recursively check sites for links to other sites, which are then also
checked for links to other sites, etc. So, if site Y links to site X,
that piece of information is saved, and if site X has not been checked
yet, it will be crawled just like site Y was. For this to work, one
must specify one or more startpages. By default, noncrawl will attempt
to crawl several sites simultaneously using threading, but this can be
disabled. It is also possible to set a limit to the number of threads.

License
=======
noncrawl is free software under the terms of the GNU General Public
License version 3 (or any later version). The author of noncrawl is
Niels Serup, contactable at ns@metanohi.org. This is version 0.1 of
the program.

External libraries included with noncrawl are GPL-compatible.

Installing
==========
Way #1
------
Just run this (requires that you have python-setuptools installed)::

  $ sudo easy_install noncrawl

Way #2
------
Get newest version of noncrawl at
http://metanohi.org/projects/noncrawl/ or at
http://pypi.python.org/pypi/noncrawl

Extract the downloaded file and run this in a terminal::

  $ sudo python setup.py install


Dependencies
============
noncrawl has no real dependencies not included in a default Python
install. Python 2.5+ is probably required, though.

Optional extras
---------------
If present, noncrawl will use these Python modules:

``htmlentitiesdecode``
 Web address: http://pypi.python.org/pypi/htmlentitiesdecode/
   $ sudo easy_install htmlentitiesdecode

(A copy of this module is included in the noncrawl distribution, so
you'll be fine without it)

``setproctitle``
 Web address: http://pypi.python.org/pypi/setproctitle/
   $ sudo easy_install setproctitle

``termcolor`` (recommended)
  Web address: http://pypi.python.org/pypi/termcolor
    $ sudo easy_install termcolor


Running
=======
noncrawl consists of two parts: the crawler and the parser. The
crawler must be accessed using a command-line utility called
``noncrawler``. Extracting information from projects can be done
either on the command-line using the ``noncrawlget`` script or by
importing the ``noncrawl.parser`` module in a Python program.

``noncrawler``
--------------
``noncrawler`` can be run like this::

  $ noncrawler [options] startpages

noncrawler has several options. Run ``noncrawler --help`` to see a
list of them. When creating a new noncrawl project, noncrawler will
create a directory in which all data will be saved. All projects can
be resumed if they have been saved properly (which should always
happen). White-and-black-listing is supported using line-separated
regular expressions with keywords. The syntax of these expressions
will be described in a moment.

``noncrawlget``
---------------
``noncrawlget`` can be run like this::

  $ noncrawlget [options] expression

The program then looks for entries that match the expression. The
syntax of these expressions is explained in the next subsection.

Expressions
-----------
The expressions used by noncrawl consists of operator-separated
two-word-groups consisting of one keyword and one Python regular
expression or one string with UNIX-style wildcards prefixed with an
'*', with everything eventually prefixed with a negating character.

An expression looks like this:
[y|n] (filter regex|wildcards [operator])+

"y" or "n" specifies whether to accept the result of a match or
not. If there is a match between the regex/wildcards and a string,
using a "n" negates the return value. It is optional to set this
keyword, and it defaults to "y", meaning that results are not
modified.

Filters in groups signify how string testing for matches should be
filtered. "url" means not changing them, "domain" means extracting the
domain name from the url and using that.

Regular expressions can be studied in the Python documentation at
http://docs.python.org/library/re.html

Strings with wildcards should be parsable by the Python fnmatch
module, documented at http://docs.python.org/library/fnmatch.html

Operators can be either &&, meaning logical AND, or ||, meaning
logical OR.

Expressions beginning with a '#' character are ignored completely.

Note that black-and-white lists prioritize non-negating
expressions. That is, specifying an expression that blacklists all
urls in existence doesn't overrule an expression that whitelists
something.

Examples
~~~~~~~~
The following expressions examplify what is possible::

  # Disallow everything using the wildcard '*' (prefixed by another
  # '*' because it's not a regular expression)
  n url **

  # Disallow search pages because of their dynamic nature
  n url .+?\?.*?q=.*

  # Still disallow them, but only on one site
  n url .+?\?.*?q=.* && domain example.com

  # Allow urls containing the string "examples" on example.com, or
  # something similar on Wikipedia.
  domain example.com && url **examples* || domain wikipedia.org && url **wiki*

  # Allow all example.* domains except for .org
  domain .*?example\.(?!org)

noncrawl comes with a base inclusion-exclusion list that it uses per
default. For more examples, see the list in the file named
"whiteblacklist.py" of this distribution.


Developing
==========
Naghni uses Git for branches. To get the latest branch, get it from
gitorious.org like this::

  $ git clone git://gitorious.org/noncrawl/noncrawl.git

noncrawl is written in Python.


The logo
========
The logo of noncrawl, found in the "logo" directory, is available
under the terms of the Creative Commons Attribution-ShareAlike 3.0 (or
any later version) Unported license. A copy of this license is
available at http://creativecommons.org/licenses/by-sa/3.0/


This document
=============
Copyright (C) 2010  Niels Serup

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
