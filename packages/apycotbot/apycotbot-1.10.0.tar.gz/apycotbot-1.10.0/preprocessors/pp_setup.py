"""installation preprocessor using distutils setup.py

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"


import os
import shutil
from os.path import join, exists, abspath

from logilab.common import optik_ext as opt
from logilab.common.contexts import pushd

from apycotbot import register, SetupException
from apycotbot.utils import EnvironmentTrackerMixin, Command
from apycotbot.preprocessors import BasePreProcessor


class DistutilsProcessor(EnvironmentTrackerMixin, BasePreProcessor):#SetPythonEnvProcessor):
    """python setup.py pre-processor

       Use a distutils'setup.py script to install a Python package. The
       setup.py should provide an "install" function which run the setup and
       return a "dist" object (i.e. the object return by the distutils.setup
       function). This preprocessor may modify the PATH and PYTHONPATH
       environment variables.
    """
    id = 'python_setup'
    _python_path_set = None
    _installed = set()

    options_def = [{'name': 'quiet',
                    'type': 'yn',
                    'default': 'no',
                    'help': "Non verbose ouput for setup.py",
                   },
                  ]


    def __init__(self, writer, options):
        EnvironmentTrackerMixin.__init__(self)
        BasePreProcessor.__init__(self, writer, options)

    def set_env(self, test):
        if not DistutilsProcessor._python_path_set:
            path = test.project_path()
            py_lib_dir = join(os.getcwd(), 'local', 'lib', 'python')
            # setuptools need this directory to exists
            if not exists(py_lib_dir):
                os.makedirs(py_lib_dir)
            self.update_env(path, 'PYTHONPATH', py_lib_dir, os.pathsep)
            DistutilsProcessor._python_path_set = py_lib_dir
            bin_dir = join(os.getcwd(), 'bin')
            self.update_env(path, 'PATH', bin_dir, os.pathsep)
        return DistutilsProcessor._python_path_set

    # PreProcessor interface ##################################################

    def test_setup(self, test):
        """setup the test environment for the main test"""
        # must be done  before _install in case setuptools is used
        self.set_env(test)
        self._install(test, test.project_path())

    def dependency_setup(self, test, path):
        """setup the test environment for a dependancy

        may raise a SetupException
        """
        # must be done  before _install in case setuptools is used
        self.set_env(test)
        self._install(test, path)

    # private #################################################################

    def _install(self, test, path):
        """run the distutils setup.py install method on a path if
        the path is not yet installed
        """
        # cache to avoid multiple installation of the same module
        if path in self._installed:
            return
        if not exists(join(path, 'setup.py')):
            raise SetupException('No file %s' % abspath(join(path, 'setup.py')))
        self._installed.add(path)
        cmd_args = ['python', 'setup.py', 'install', '--home',
                    join(test.tmpdir, 'local')]
        if opt.check_yn(None, 'quiet', self.get_option('quiet')):
            cmd_args.append('--quiet')
        with pushd(path):
            cmd = Command(self.writer, cmd_args, raises=True)
            cmd.run()
            if exists('build'):
                shutil.rmtree('build') # remove the build directory


register('preprocessor', DistutilsProcessor)
