import tarfile
from tempfile import mkdtemp
from shutil import copy, rmtree
from os.path import abspath, join, isdir, isfile
from os import mkdir, remove

from setuptools import setup, find_packages


name = 'pysistence'
version = '0.3.0'
base_name = '%s-%s' % (name, version)
tarball_name = '%s.tar.gz' % base_name

setup(
    name=name,
    packages=find_packages('source'),
    package_dir = {'':'source'},
    version=version,
    url="http://packages.python.org/pysistence",
    description='A set of functional data structures for Python',
    long_description='Pysistence is a library that seeks to bring functional data structures to Python.',
    author="Jason Baker",
    author_email="amnorvend@gmail.com",
    test_suite = 'nose.collector',
    tests_require = ['nose', 'coverage'],
    license='License :: OSI Approved :: MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
