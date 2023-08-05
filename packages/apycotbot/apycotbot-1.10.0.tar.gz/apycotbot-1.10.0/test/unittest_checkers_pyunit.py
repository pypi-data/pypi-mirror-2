"""
unit tests for python test checkers
"""

import os, sys
from os.path import join

from logilab.common.testlib import unittest_main, TestCase, mock_object

from apycotbot.utils import SUCCESS, FAILURE, ERROR, PARTIAL, NODATA
from apycotbot.checkers import chks_python

from utils import MockWriter, input_path

def _test_cmd(self, cmd, status, success=0, failures=0, errors=0, skipped=0):

    for name, got, expected in (
            ('failures', cmd.parser.failures, failures),
            ('errors', cmd.parser.errors, errors),
            ('skipped', cmd.parser.skipped, skipped),
            ('success', cmd.parser.success, success),
        ):
        self.assertEquals(got, expected, '%i %s but %i expected'
                          % (got, name, expected))
    self.assertIs(cmd.status, status)

class PyUnitTestCheckerTC(TestCase):
    input_dir = input_path('testcase_pkg/tests/')

    def setUp(self):
        self.checker = chks_python.PyUnitTestChecker(MockWriter())
        self.checker._coverage = None
        self.checker._path = input_path('')

    def input_path(self, path):
        return join(self.input_dir, path)

    def test_run_test_result_empty(self):
        cmd = self.checker.run_test(self.input_path('unittest_empty.py'))
        _test_cmd(self, cmd, NODATA, success=0)

    def test_run_test_result_no_main(self):
        cmd = self.checker.run_test(self.input_path('unittest_no_main.py'))
        _test_cmd(self, cmd, NODATA, success=0)

    def test_run_test_result_success(self):
        cmd = self.checker.run_test(self.input_path('unittest_success.py'))
        _test_cmd(self, cmd, SUCCESS, success=1)

    def test_run_test_result_failure(self):
        cmd = self.checker.run_test(self.input_path('unittest_failure.py'))
        _test_cmd(self, cmd, FAILURE, failures=1)

    def test_run_test_result_error(self):
        cmd = self.checker.run_test(self.input_path('unittest_errors.py'))
        _test_cmd(self, cmd, FAILURE, errors=1)

    def test_run_test_result_skipped(self):
        cmd = self.checker.run_test(self.input_path('unittest_skip.py'))
        _test_cmd(self, cmd, PARTIAL, skipped=1)

    def test_run_test_result_mixed(self):
        cmd = self.checker.run_test(self.input_path('unittest_mixed.py'))
        _test_cmd(self, cmd, FAILURE, 2, 15, 1, 2)

    def test_run_test_result_mixed_std(self):
        cmd = self.checker.run_test(self.input_path('unittest_mixed_std.py'))
        _test_cmd(self, cmd, FAILURE, 2, 15, 1, 0)


class PyTestCheckerTC(TestCase):
    input_dir = input_path('testcase_pkg/tests/')

    def setUp(self):
        self.checker = chks_python.PyTestChecker(MockWriter())
        self.checker._coverage = False
        self.cwd = os.getcwd()
        os.chdir(input_path('testcase_pkg'))

    def tearDown(self):
        os.chdir(self.cwd)

    def _test_cmd(self, *args):

        cmd_args = ['-c', 'from logilab.common.pytest '
                  'import run; run()',]
        cmd_args.extend(args)
        return self.checker.run_test(cmd_args, sys.executable)

    def test_global(self):
        cmd = self._test_cmd()
        #XXX should be NODATA but not handle at the moment
        _test_cmd(self, cmd, FAILURE, 6, 31, 3, 3)

if __name__ == '__main__':
    unittest_main()
