#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple utility to calculate different types of hashes from given files/data
"""

from __future__ import print_function, unicode_literals

import argparse
import fileinput
import hashlib
import os
import sys
import zlib

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

__version__ = '2.1.5'

MAX_INPUT_READ = 4*1024**2
DEFAULT_ALGORITHM = 'sha1'
E_OK = 0
E_FAIL = 1
E_FAIL_NO_FILES = 2
VERIFICATION_OK = 'OK'
VERIFICATION_FAIL = 'FAILED'


PY3 = sys.version_info >= (3, 0)

# pylint: disable=missing-docstring
def _get_available_hash_algorithms():
    try:
        available = hashlib.algorithms_available
    except AttributeError:
        try:
            available = set(hashlib.algorithms)
        except AttributeError:
            available = {'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'}

    aliases = {
        'sha1': {'DSA', 'DSA-SHA', 'dsaEncryption', 'dsaWithSHA', 'ecdsa-with-SHA1'}
    }

    for name in aliases:
        if name in available:
            available -= aliases[name]

    to_remove = set()
    for algo in available:
        lowered = algo.lower()
        if algo != lowered and lowered in available:
            to_remove.add(algo)

    available -= to_remove
    return available

AVAILABLE_HASH_ALGORITHMS = _get_available_hash_algorithms()
AVAILABLE_CHECKSUM_ALGORITHMS = {'crc32', 'adler32'}
AVAILABLE_ALGORITHMS = sorted(AVAILABLE_HASH_ALGORITHMS | AVAILABLE_CHECKSUM_ALGORITHMS)


def checksum_file(file_path, algo, max_input_read=4*1024**2):
    """
    Calculate checksum
    :param file_path: path or '-' for STDIN
    :param algo:
    :param max_input_read:
    :return:
    """
    if algo not in AVAILABLE_CHECKSUM_ALGORITHMS:
        raise ValueError("Unknown algorithm: %s" % algo)

    value = 0
    hasher = getattr(zlib, algo)

    fh = open(file_path, 'rb') if file_path != '-' else sys.stdin
    while True:
        data = fh.read(max_input_read)
        if not len(data):
            break

        value = hasher(data, value)

    if file_path != '-':
        fh.close()

    value = value & 0xffffffff
    return hex(value)[2:]


def hash_file(file_path, algo, max_input_read=4*1024**2):
    """
    Calculate hash
    :param file_path: path or '-' for STDIN
    :param algo:
    :param max_input_read:
    :return:
    """
    hasher = hashlib.new(algo)

    if file_path == '-': # sys.stdin
        fh = sys.stdin
        if PY3:
            fh = fh.buffer

        while True:
            data = fh.read(max_input_read)
            if not len(data):
                break

            hasher.update(data)

    else:
        fh = open(file_path, 'rb')

        while True:
            data = fh.read(max_input_read)
            if not len(data):
                break

            hasher.update(data)

        fh.close()

    return hasher.hexdigest()


def _get_file_helpers():
    helpers = {algo: hash_file for algo in AVAILABLE_HASH_ALGORITHMS}
    helpers.update({algo: checksum_file for algo in AVAILABLE_CHECKSUM_ALGORITHMS})
    return helpers

FILE_HELPERS = _get_file_helpers()


OPENED_FILES = {'succes': 0, 'fail': 0}
def fileinput_openhook_safe(name, mode):
    try:
        fh = open(name, mode)
    except Exception as exc:
        OPENED_FILES['fail'] += 1
        print('%s: cannot open (%s)' % (name, exc.args[1]))
        return StringIO()
    else:
        OPENED_FILES['succes'] += 1
        return fh


def mode_generate_algo_symlinks(args):
    """
    Print commmands to create symlinks for hashfile for every known algorithm
    :return:
    """
    current = os.path.realpath(sys.argv[0])
    bindir = os.path.dirname(current)
    for algo in AVAILABLE_ALGORITHMS:
        print('ln -s %s %s' % (current, os.path.join(bindir, algo)))

    return E_OK


def mode_calculate(args):
    """
    Calculate hases and pront them to stdout
    :param args:
    :return:
    """
    for i, filename in enumerate(args.files):
        algo = args.algorithm[i] if len(args.algorithm) > i else args.algorithm[-1]

        file_helper = FILE_HELPERS[algo]
        try:
            filehash = file_helper(filename, algo=algo, max_input_read=args.max_input_read)
        except (OSError, IOError) as exc:
            print('ERROR: %s %s' % (filename, str(exc)), file=sys.stderr)
        else:
            print('%s: %s %s' % (algo, filehash, filename))

    return E_OK


def mode_check(args):
    """
    Verify calculated checksums
    :param args:
    :return:
    """
    if not args.files or args.files == ['-']:
        print('ERROR: no files to check specified', file=sys.stderr)
        sys.exit(1)

    def _quiet(inp1, inp2):
        if inp1 != inp2:
            print('%s: %s' % (filename, VERIFICATION_FAIL))
            return
        return True

    def _verbose(inp1, inp2):
        if inp1 == inp2:
            print('%s: %s' % (filename, VERIFICATION_OK))
        else:
            print('%s: %s' % (filename, VERIFICATION_FAIL))

        return True

    def _status(inp1, inp2):
        if inp1 != inp2:
            sys.exit(E_FAIL)

        return True

    if args.quiet:
        verifier = _quiet
    elif args.status:
        verifier = _status
    else:
        verifier = _verbose

    exit_code = E_OK

    for line in fileinput.input(args.files, openhook=fileinput_openhook_safe):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        try:
            algo, expected_filehash = line.split(': ', 1)
            expected_filehash, filename = expected_filehash.split(' ')
        except ValueError:
            if args.warn:
                print('ERROR: %s Incorrect format' % (fileinput.filename()), file=sys.stderr)
            continue

        file_helper = FILE_HELPERS[algo]
        try:
            filehash = file_helper(filename, algo=algo, max_input_read=args.max_input_read)
        except (OSError, IOError) as exc:
            print('ERROR: %s %s' % (filename, str(exc)), file=sys.stderr)
        else:
            if not verifier(filehash, expected_filehash):
                exit_code = E_FAIL
    if exit_code == E_OK and OPENED_FILES['fail'] > 0:
        exit_code = E_FAIL_NO_FILES
    return exit_code


def mode_default(args):
    """
    Do nothing
    :param args:
    :return:
    """
    return E_OK


def parse_args(argv):
    """
    Parse input params
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser(description='Calculate hash of some files',
        epilog='Algorithm can be also set from program name (for example call program as sha1 to use sha1 algorithm)')
    parser.add_argument('--algorithm', '-a', default=[], action='append', choices=AVAILABLE_ALGORITHMS,
        help='algorithm used to calculate hash '
             'If given more then one, then use different algorithms for different files (use first algo to first '
             'file, second algo to second file etc. If there is more files then algorithms, last algorithm from '
             'list is used.')
    parser.add_argument('--generate-algo-symlinks', action='store_const', dest='mode', const='generate-algo-symlinks',
        help='Show aliases for every algorithm handled by hashfile')
    # http://linux.die.net/man/1/md5sum
    parser.add_argument('--check', '-c', action='store_const', dest='mode', const='check',
        help='read checksums from the FILEs and check them ')
    parser.add_argument('--quiet', '-q', action='store_true',
        help='don\'t print OK for each successfully verified file')
    parser.add_argument('--status', '-s', action='store_true',
        help='don\'t output anything, status code shows success')
    parser.add_argument('--warn', '-w', action='store_true',
        help='warn about improperly formatted checksum lines')
    parser.add_argument('--max-input-read', default=MAX_INPUT_READ,
        help='maximum data size for read at once')
    parser.add_argument('files', metavar='FILE', type=str, nargs='*',
        help='list of files (stdin by default)')
    parser.add_argument('--version', '-v', action="version", version="%%(prog)s %s" % __version__)

    parser.set_defaults(mode='calculate')

    args = parser.parse_args()


    if args.mode != 'check' and (args.quiet or args.status or args.warn):
        parser.error('--quiet, --status and --warn options are available only with --check option')

    if len(args.algorithm) > 0:
        pass
    elif os.path.basename(sys.argv[0]) in AVAILABLE_ALGORITHMS:
        args.algorithm = [os.path.basename(sys.argv[0]), ]
    else:
        args.algorithm = [DEFAULT_ALGORITHM, ]

    if not args.files:
        args.files = ['-']
    # PYTHON2
    elif hasattr(args.files[0], 'decode'):
        args.files = [filename.decode('utf-8') for filename in args.files]

    return args


# pylint: disable=missing-docstring
def main():
    args = parse_args(sys.argv[1:])

    modes = {
        'calculate': mode_calculate,
        'check': mode_check,
        'generate-algo-symlinks': mode_generate_algo_symlinks,
    }
    handler = modes.get(args.mode, mode_default)
    exit_code = handler(args)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
