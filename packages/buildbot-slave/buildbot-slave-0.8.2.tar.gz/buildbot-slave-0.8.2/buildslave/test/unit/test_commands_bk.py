import os

from twisted.trial import unittest
from twisted.python import runtime

from buildslave.test.fake.runprocess import Expect
from buildslave.test.util.sourcecommand import SourceCommandTestMixin
from buildslave.commands import bk

class TestBK(SourceCommandTestMixin, unittest.TestCase):

    def setUp(self):
        self.setUpCommand()

    def tearDown(self):
        self.tearDownCommand()

    def test_simple(self):
        self.patch_getCommand('bk', 'path/to/bk')
        self.clean_environ()
        self.make_command(bk.BK, dict(
            workdir='workdir',
            mode='copy',
            revision='1.114',
            bkurl='http://bkdemo.bkbits.net/bk_demo1',
        ))

        exp_environ = dict(PWD='.', LC_MESSAGES='C')
        expects = [
            Expect([ 'clobber', 'workdir' ],
                self.basedir)
                + 0,
            Expect([ 'clobber', 'source' ],
                self.basedir)
                + 0,
                Expect(['path/to/bk', 'clone', '-r1.114',
                        'http://bkdemo.bkbits.net/bk_demo1', 'source'],
                self.basedir,
                sendRC=False, timeout=120, usePTY=False)
                + 0,
            Expect(['path/to/bk', 'changes', '-r+', '-d:REV:'],
                self.basedir_source,
                sendRC=False, usePTY=False, timeout=120, sendStderr=False,
                sendStdout=False, keepStdout=True, environ=exp_environ)
            + { 'stdout' : '1.114\n' } # TODO: is this what BK outputs?
                + 0,
            Expect([ 'copy', 'source', 'workdir'],
                self.basedir)
                + 0,
        ]
        self.patch_runprocess(*expects)

        d = self.run_command()
                # TODO: why the extra quotes?
        d.addCallback(self.check_sourcedata, '"http://bkdemo.bkbits.net/bk_demo1\n"')
        return d
