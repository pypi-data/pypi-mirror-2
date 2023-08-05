import commands
import os
import re
import shutil
import tempfile

from zope.testing import renormalizing
import z3c.testsetup

import sdistmaker.maker

checker = renormalizing.RENormalizing([
    (re.compile(r'\S+/pypi'), 'PYPI'),
    (re.compile(r'\S+/bin/python'), 'python'),
    ])


def setup(test):
    #Monkeypatching to prevent real action from taking place:
    test.output_results = ['']

    def mock_getstatusoutput(cmd):
        print "Command:", cmd
        return 0, test.output_results.pop(0)

    test.orig_getstatusoutput = commands.getstatusoutput
    commands.getstatusoutput = mock_getstatusoutput

    def mock_copy(src, dest):
        print "Mock copy %s -> %s" % (src, dest)
        open(dest, 'w').write('mock')

    test.orig_copy = shutil.copy
    shutil.copy = mock_copy

    def mock_find_tarball(dist_dir, name, version):
        return name + '-' + version + '.tar.gz'

    test.orig_find_tarball = sdistmaker.maker.find_tarball
    sdistmaker.maker.find_tarball = mock_find_tarball

    test.tempdir = tempfile.mkdtemp()
    test.pypidir = os.path.join(test.tempdir, 'pypi')
    os.mkdir(test.pypidir)
    test.globs.update({'pypidir': test.pypidir,
                       'output_results': test.output_results,
                       })


def teardown(test):
    # Restore originals:
    commands.getstatusoutput = test.orig_getstatusoutput
    shutil.copy = test.orig_copy
    sdistmaker.maker.find_tarball = test.orig_find_tarball


test_suite = z3c.testsetup.register_all_tests(
    'sdistmaker',
    checker=checker)
