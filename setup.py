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


from codecs import open
from os import path
from setuptools import setup, find_packages


BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hashfile',
    version='1.0.0',
    description='calculate hash or checksum',
    long_description=long_description,
    url='http://msztolcman.github.io/hashfile/',
    author='Marcin Sztolcman',
    author_email='marcin@urzenia.net',
    license='MIT',

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
    install_requires=['argparse'],
    packages=find_packages(),

    keywords=['security', 'hash', 'checksum', 'sha1', 'md5', 'sha224', 'sha256', 'sha384', 'sha512', 'crc32', 'adler32',
        'md4', 'mdc2', 'ripemd160', 'sha', 'whirlpool'],

    entry_points={
        'console_scripts': [
            'hashfile=hashfile:main',
        ],
    },
)

