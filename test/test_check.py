#!/usr/bin/env python

import re

from helpers import *

def test_no_arguments():
    ret = call_hashfile('-c')

    assert ret.code == 1
    assert ret.stdout == ''
    assert ret.stderr == 'ERROR: no files to check specified\n'


def test_single_file_valid():
    check_file, data_files = create_check_file({'aaa': 'sha1'})

    ret = call_hashfile('-c', check_file)

    assert ret.code == 0
    assert ret.stdout == '%s: OK\n' % data_files[0]
    assert ret.stderr == ''


def test_three_files_valid():
    check_file1, data_files1 = create_check_file({'aaa1': 'sha1', 'bbb1': 'sha1'})
    check_file2, data_files2 = create_check_file({'ddd': 'md4'})
    check_file3, data_files3 = create_check_file({'aaa2': 'sha1', 'bbb2': 'sha1', 'ccc': 'md5'})

    ret = call_hashfile('-c', check_file1, check_file2, check_file3)

    assert ret.code == 0
    assert ret.stdout == '''%s: OK\n%s: OK\n%s: OK\n%s: OK\n%s: OK\n%s: OK\n''' % (
        data_files1[0], data_files1[1], data_files2[0], data_files3[0], data_files3[1], data_files3[2])
    assert ret.stderr == ''


def test_single_file_invalid():
    check_file, data_files = create_check_file({'aaa': '!sha1:invalid-checksum'})

    ret = call_hashfile('-c', check_file)

    assert ret.code == 0
    assert ret.stdout == '%s: FAILED\n' % data_files[0]
    assert ret.stderr == ''


def test_three_files_invalid():
    check_file1, data_files1 = create_check_file({'aaa1': '!sha1:invalid-checksum', 'bbb1': '!sha1:invalid-checksum'})
    check_file2, data_files2 = create_check_file({'ddd': '!md4:invalid-checksum'})
    check_file3, data_files3 = create_check_file({
        'aaa2': '!sha1:invalid-checksum',
        'bbb2': '!sha1:invalid-checksum',
        'ccc': '!md5:invalid-checksum'})

    ret = call_hashfile('-c', check_file1, check_file2, check_file3)

    assert ret.code == 0
    assert ret.stdout == '''%s: FAILED\n%s: FAILED\n%s: FAILED\n%s: FAILED\n%s: FAILED\n%s: FAILED\n''' % (
        data_files1[0], data_files1[1], data_files2[0], data_files3[0], data_files3[1], data_files3[2])
    assert ret.stderr == ''


def test_three_files_mixed():
    check_file1, data_files1 = create_check_file({'aaa1': 'sha1', 'bbb1': '!sha1:invalid-checksum'})
    check_file2, data_files2 = create_check_file({'ddd': 'md4'})
    check_file3, data_files3 = create_check_file({
        'aaa2': 'sha1',
        'bbb2': '!sha1:invalid-checksum',
        'ccc': 'md5'})

    ret = call_hashfile('-c', check_file1, check_file2, check_file3)

    assert ret.code == 0
    assert ret.stdout == '''%s: OK\n%s: FAILED\n%s: OK\n%s: OK\n%s: FAILED\n%s: OK\n''' % (
        data_files1[0], data_files1[1], data_files2[0], data_files3[0], data_files3[1], data_files3[2])
    assert ret.stderr == ''


def test_file_not_exists():
    ret = call_hashfile('-c', '/not/exists')

    assert ret.code == 2
    assert re.match(r'^/not/exists: cannot open (.*)\n', ret.stdout)
    assert ret.stderr == ''


def test_file_existent_mixed():
    check_file, data_files = create_check_file({'aaa1': 'sha1', 'bbb1': 'sha1'})
    ret = call_hashfile('-c', '/not/exists', check_file)

    assert ret.code == 2
    assert re.match(r'^/not/exists: cannot open (.*)\n%s: OK\n%s: OK' % (data_files[0], data_files[1]), ret.stdout)
    assert ret.stderr == ''
