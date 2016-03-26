#!/usr/bin/env python

import os
import re

from helpers import *


def test_no_arguments_stdin():
    ret = call_hashfile(stdin='asd')

    print(ret.stderr)
    assert ret.code == 0
    assert ret.stdout == 'sha1: f10e2821bbbea527ea02200352313bc059445190 -\n'
    assert re.match('^$', ret.stderr)


def test_one_file_default_algo():
    data_file = create_calculate_file('asd')
    ret = call_hashfile(data_file)
    safe_unlink(data_file)

    assert ret.code == 0
    assert re.match(r'^sha1: f10e2821bbbea527ea02200352313bc059445190 .+', ret.stdout)
    assert re.match('^$', ret.stderr)


def test_three_files_default_algo():
    data_file1 = create_calculate_file('asds')
    data_file2 = create_calculate_file('asqwe')
    data_file3 = create_calculate_file('111ss')
    ret = call_hashfile(data_file1, data_file2, data_file3)
    safe_unlink(data_file1)
    safe_unlink(data_file2)
    safe_unlink(data_file3)

    assert ret.code == 0
    assert re.match(r'''^sha1: 43922098ffd36010ad90d47fe2b099853a2ab1aa %s
sha1: 7f1da4ad6226082731c128738597295539373cf0 %s
sha1: c92e11e5dde3bb51826c7e969bbb78f0fb1fcea0 %s''' % (
        re.escape(data_file1),
        re.escape(data_file2),
        re.escape(data_file3)), ret.stdout)
    assert re.match('^$', ret.stderr)


def test_one_file_single_algo():
    data_file = create_calculate_file('asd')
    ret = call_hashfile('-a', 'sha256', data_file)
    safe_unlink(data_file)

    assert ret.code == 0
    assert re.match(r'^sha256: 688787d8ff144c502c7f5cffaafe2cc588d86079f9de88304c26b0cb99ce91c6 %s' %
        re.escape(data_file), ret.stdout)
    assert re.match('^$', ret.stderr)


def test_three_files_single_algo():
    data_file1 = create_calculate_file('asds')
    data_file2 = create_calculate_file('asqwe')
    data_file3 = create_calculate_file('111ss')
    ret = call_hashfile('-a', 'sha256', data_file1, data_file2, data_file3)
    safe_unlink(data_file1)
    safe_unlink(data_file2)
    safe_unlink(data_file3)

    assert ret.code == 0
    assert re.match(r'''^sha256: e5af4874d53cd94043d5292e3531c9597b3ef8940905c68ad9859c34a8d385dd %s
sha256: 82d1ed38bc3df0e52901f04eeb8f9dc40109e4514d33d5cfe71fb503ac4cf61e %s
sha256: 578a95c55beb2476defb287c8d7659affcb2a881e40f6ecff8248964df308cbc %s''' % (
        re.escape(data_file1),
        re.escape(data_file2),
        re.escape(data_file3)
    ), ret.stdout)
    assert re.match('^$', ret.stderr)


def test_three_files_two_algo():
    data_file1 = create_calculate_file('asds')
    data_file2 = create_calculate_file('asqwe')
    data_file3 = create_calculate_file('111ss')
    ret = call_hashfile('-a', 'sha256', '-a', 'md5', data_file1, data_file2, data_file3)
    safe_unlink(data_file1)
    safe_unlink(data_file2)
    safe_unlink(data_file3)

    assert ret.code == 0
    assert re.match(r'''^sha256: e5af4874d53cd94043d5292e3531c9597b3ef8940905c68ad9859c34a8d385dd %s
md5: 72eb0a4f1bb3bb2a744fdd106a504b01 %s
md5: d811775d92c1681aa1838f07b858d899 %s''' % (
        re.escape(data_file1),
        re.escape(data_file2),
        re.escape(data_file3)
    ), ret.stdout)
    assert re.match('^$', ret.stderr)


def test_three_files_three_algo():
    data_file1 = create_calculate_file('asds')
    data_file2 = create_calculate_file('asqwe')
    data_file3 = create_calculate_file('111ss')
    ret = call_hashfile('-a', 'sha256', '-a', 'md5', '-a', 'sha224', data_file1, data_file2, data_file3)
    safe_unlink(data_file1)
    safe_unlink(data_file2)
    safe_unlink(data_file3)

    assert ret.code == 0
    assert re.match(r'''^sha256: e5af4874d53cd94043d5292e3531c9597b3ef8940905c68ad9859c34a8d385dd %s
md5: 72eb0a4f1bb3bb2a744fdd106a504b01 %s
sha224: 4995bc14d789f709e120e1a073047213fa5a014afe78539c2befc7f1 %s''' % (
        re.escape(data_file1),
        re.escape(data_file2),
        re.escape(data_file3)
    ), ret.stdout)
    assert re.match('^$', ret.stderr)


def test_three_files_single_algo_no_access_to_file():
    data_file1 = create_calculate_file('asds')
    data_file2 = create_calculate_file('asqwe')
    data_file3 = create_calculate_file('111ss')
    os.chmod(data_file2, 0)
    ret = call_hashfile('-a', 'sha256', data_file1, data_file2, data_file3)
    safe_unlink(data_file1)
    safe_unlink(data_file2)
    safe_unlink(data_file3)

    print(ret)
    assert ret.code == 0
    assert re.match(r'''^sha256: e5af4874d53cd94043d5292e3531c9597b3ef8940905c68ad9859c34a8d385dd %s
sha256: 578a95c55beb2476defb287c8d7659affcb2a881e40f6ecff8248964df308cbc %s''' % (
        re.escape(data_file1),
        re.escape(data_file3)
    ), ret.stdout)
    assert re.match(r'''ERROR: %s \[Errno 13\] Permission denied: .+''' % (re.escape(data_file2)), ret.stderr)


def test_unallowed_arguments():
    for arg in ('--quiet', '--warn', '--status'):
        ret = call_hashfile(arg, stdin='asd')

        assert ret.code == 2
        assert ret.stdout == ''
        assert re.match(r'^usage: ', ret.stderr)
