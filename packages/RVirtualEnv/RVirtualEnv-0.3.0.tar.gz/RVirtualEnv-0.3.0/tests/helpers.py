
import os
from os import path
from shutil import rmtree
from unittest import TestCase
from tempfile import mkdtemp
import distutils.command.install

import rvirtualenv


class InTempTestCase(TestCase):
    def setUp(self):
        # store curr path
        self.oldcwd = os.getcwd()

        # create test dir structure
        self.directory = mkdtemp(prefix='test_rvirtualenv_')

        # new rvirtualenv
        self.virtualenv = path.join(self.directory, 'PY')

        # store base dir
        self.base = path.join(path.dirname(__file__), path.pardir)

    def tearDown(self):
        # go back
        os.chdir(self.oldcwd)

        # dir cleanup
        rmtree(self.directory, True)

def store_directory_structure(mypath, content=None):
    '''
    recursivelly traverse directory and store it in format:
    (
      (mypath, None),
      (mypath/to, None),
      (mypath/to/dir, None),
      (mypath/to/dir/file.txt, {{ file's content }}),
    )
    '''
    d = {}
    for base, dirs, files in os.walk(mypath):
        d[base] = None
        for i in files:
            fn = path.join(base, i)
            if content is not None:
                d[fn] = content
                continue
            f = open(fn, 'rb')
            d[fn] = f.read()
            f.close()
    return d.items()

def relpath(p, start):
    "os.path.relpath dummy replacement"
    return p.replace(path.join(start, ''), '', 1)

