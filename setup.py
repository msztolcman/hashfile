import pkg_resources
import platform
import sys


def validate_python_version():
    """
    Validate python interpreter version. Only 3.3+ allowed.
    """
    if pkg_resources.parse_version(platform.python_version()) < pkg_resources.parse_version('2.7.0'):
        print("Sorry, Python 2.7+ is required")
        sys.exit(1)
validate_python_version()


import codecs
import os.path
from setuptools import setup


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hashfile',
    version='2.1.5',
    description='calculate hash or checksum',
    long_description=long_description,
    url='http://msztolcman.github.io/hashfile/',
    author='Marcin Sztolcman',
    author_email='marcin@urzenia.net',
    license='MIT',

    packages=['hashfile'],
    package_data={'': ['LICENSE', 'VERSION']},
    package_dir={'hashfile': 'hashfile'},
    include_package_data=True,
    install_requires=['argparse'],

    keywords=['security', 'hash', 'checksum',
        'sha', 'sha1', 'md5', 'sha224', 'sha256', 'sha384', 'sha512',
        'crc32', 'adler32',
        'md4', 'mdc2', 'ripemd160', 'whirlpool'],

    entry_points={
        'console_scripts': [
            'hashfile=hashfile:main',
        ],
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

