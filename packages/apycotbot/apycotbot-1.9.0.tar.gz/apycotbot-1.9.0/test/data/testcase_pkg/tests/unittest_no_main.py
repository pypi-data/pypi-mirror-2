import unittest

class DummyTest(unittest.TestCase):
    def runTest(self):
        pass

def Run(runner=None):
    testsuite = unittest.TestSuite()
    testsuite.addTest(DummyTest())

    if runner is None:
        runner = unittest.TextTestRunner()
    return runner.run(testsuite)
