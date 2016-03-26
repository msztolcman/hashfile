#!/usr/bin/env python3

import collections
import hashlib

import os
import subprocess
import tempfile

__all__ = ['ProcResult', 'call_hashfile', 'create_calculate_file', 'create_check_file', 'safe_unlink']

ProcResult = collections.namedtuple('ProcResult', ['code', 'stdout', 'stderr'])


def call_hashfile(*args, **kwargs):
    cmd = list(args)
    cmd.insert(0, 'hashfile')

    stdin = kwargs.get('stdin', None)
    if stdin is not None:
        stdin = stdin.encode()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE if stdin is not None else None)
    (stdout, stderr) = proc.communicate(stdin)

    if hasattr(stdout, 'decode'):
        stdout = stdout.decode('utf-8')

    if hasattr(stderr, 'decode'):
        stderr = stderr.decode('utf-8')

    proc_result = ProcResult(proc.returncode, stdout, stderr)
    return proc_result


def create_calculate_file(data):
    if data:
        data = data.encode()

    with tempfile.NamedTemporaryFile(delete=False) as fh:
        fh.write(data)

    return fh.name


def create_check_file(data):
    data_files = []
    with tempfile.NamedTemporaryFile(delete=False) as fh:
        values = sorted(data.keys())

        for value in values:
            algo = data[value]
            data_file = create_calculate_file(value)
            data_files.append(data_file)
            if algo.startswith('!'):
                algo, hash_file = algo[1:].split(':', 1)
            else:
                if hasattr(value, 'encode'):
                    value = value.encode()
                hash_file = hashlib.new(algo, value).hexdigest()
            value = '%s: %s %s\n' % (algo, hash_file, data_file)
            fh.write(value.encode())

    return fh.name, data_files


def safe_unlink(path):
    try:
        os.remove(path)
    except:
        pass


