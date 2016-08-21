hashfile
========

``hashfile`` calculates hashes or checksums in many formats, also verify
them.

Default algorithm is ``sha1``. This can be changed by passing argument
``-a``/``--algorithm`` to ``hashfile``, or by calling ``hashfile`` with
algorithm name (ie. using symlinks).

``hashfile`` works pretty well with big files, because always read data
partially, by default 4MB of data at once (it can be changed using
``--max-input-read`` param).

Examples
--------

::

    # simplest call
    % hashfile /etc/hosts
    sha1: 4f53fb6efebddfdbe989f3bff980cd07ebcdc6bb /etc/hosts

    # specify algorithm
    % hashfile -a md5 /etc/hosts
    md5: 71e875e9d194c18567f48cf9534ed6cf /etc/hosts

    # one file, many algorithms
    % hashfile -a md5 -a sha1 /etc/hosts /etc/hosts
    md5: 71e875e9d194c18567f48cf9534ed6cf /etc/hosts
    sha1: 4f53fb6efebddfdbe989f3bff980cd07ebcdc6bb /etc/hosts

    # many files, other algorithm for each one
    % hashfile -a md5 -a sha1 /etc/hosts /etc/shells
    md5: 71e875e9d194c18567f48cf9534ed6cf /etc/hosts
    sha1: e0de09cb8797a4d39f89049d74585e815a3c6ceb /etc/shells

    # many files, one algorithm
    % hashfile -a sha256 /etc/hosts /etc/shells
    sha256: 48127a192d62fdcaa39f7cebd1ea5f3fe660807c8cd3a92599406d16bddc341a /etc/hosts
    sha256: edfd1953cce18ab14449b657fcc01ece6a43a7075bab7b451f3186b885c20998 /etc/shells

    # choose algorithm using symlinks
    % ln -s `which hashfile` ~/bin/sha256
    % sha256 /etc/hosts
    sha256: 48127a192d62fdcaa39f7cebd1ea5f3fe660807c8cd3a92599406d16bddc341a /etc/hosts

    # create verify file, and then verify
    % hashfile -a sha256 README.* > check.sum
    % hashfile -c check.sum
    README.md: OK
    README.rst: OK

Current stable version
----------------------

2.1.5

Python version
--------------

``hashfile`` works with Python 2.7+ and 3.3+.

Usage
-----

Everything is in help :) Just execute:

::

    hashfile --help

Look at result (remember: list of algorithms may vary on your system):

::

    % hashfile --help
    usage: hashfile [-h]
                    [--algorithm {adler32,crc32,md4,md5,mdc2,ripemd160,sha,sha1,sha224,sha256,sha384,sha512,whirlpool}]
                    [--generate-algo-symlinks] [--check] [--quiet] [--status]
                    [--warn] [--max-input-read MAX_INPUT_READ]
                    [FILE [FILE ...]]

    Calculate hash of some files

    positional arguments:
      FILE                  list of files (stdin by default)

    optional arguments:
      -h, --help            show this help message and exit
      --algorithm {adler32,crc32,md4,md5,mdc2,ripemd160,sha,sha1,sha224,sha256,sha384,sha512,whirlpool}, -a {adler32,crc32,md4,md5,mdc2,ripemd160,sha,sha1,sha224,sha256,sha384,sha512,whirlpool}
                            algorithm used to calculate hash If given more then
                            one, then use different algorithms for different files
                            (use first algo to first file, second algo to second
                            file etc. If there is more files then algorithms, last
                            algorithm from list is used.
      --generate-algo-symlinks
                            Show aliases for every algorithm handled by hashfile
      --check, -c           read checksums from the FILEs and check them
      --quiet, -q           don't print OK for each successfully verified file
      --status, -s          don't output anything, status code shows success
      --warn, -w            warn about improperly formatted checksum lines
      --max-input-read MAX_INPUT_READ
                            maximum data size for read at once

    Algorithm can be also set from program name (for example call program as sha1
    to use sha1 algorithm)

Installation
------------

1. Using PIP

``hashfile`` should work on any platform where
`Python <http://python.org>`__ is available, it means Linux, Windows,
MacOS X etc.

Simplest way is to use Python's built-in package system:

::

    pip install hashfile

2. Using `pipsi <https://github.com/mitsuhiko/pipsi>`__

   pipsi install hashfile

3. Using sources

Download sources from
`Github <https://github.com/msztolcman/hashfile/archive/2.1.5.zip>`__:

::

    wget -O 2.1.5.zip https://github.com/msztolcman/hashfile/archive/2.1.5.zip

or

::

    curl -o 2.1.5.zip https://github.com/msztolcman/hashfile/archive/2.1.5.zip

Unpack:

::

    unzip 2.1.5.zip

And install

::

    cd hashfile-2.1.5
    python setup.py install

Voila!

Authors
-------

Marcin Sztolcman marcin@urzenia.net

Contact
-------

If you like or dislike this software, please do not hesitate to tell me
about this me via email (marcin@urzenia.net).

If you find bug or have an idea to enhance this tool, please use
GitHub's `issues <https://github.com/msztolcman/hashfile/issues>`__.

License
-------

The MIT License (MIT)

Copyright (c) 2012 Marcin Sztolcman

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

ChangeLog
---------

v2.1.5
~~~~~~

-  fixed reading binary data from stdin

v2.1.4
~~~~~~

-  fixed working with binary files
-  hashfile is now a package
-  some package-related changes
-  few updates to Makefile

v2.1.3
~~~~~~

-  fixed working with aliases

v2.1.2
~~~~~~

-  another small improvements for PyPI
-  forgotten changelog

v2.1.1
~~~~~~

-  small improvements for setup.py and PyPI

v2.1.0
~~~~~~

-  added --version switch

v2.0.0
~~~~~~

-  added compatibility with tools like md5sum or sha1sum (verify mode,
   call arguments compatibility, etc)

v1.0.0
~~~~~~

-  First public version
