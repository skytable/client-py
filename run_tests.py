import unittest


class MyTestLoader(unittest.TestLoader):
    def loadTestsFromTestCase(self, testCaseClass):
        test_suite = super().loadTestsFromTestCase(testCaseClass)
        return test_suite

    def loadTestsFromModule(self, module, *args, **kwargs):
        test_suite = super().loadTestsFromModule(module, *args, **kwargs)
        return test_suite


class MyTestRunner(unittest.TextTestRunner):
    def run(self, test):
        self.verbosity = 2
        result = super().run(test)
        return result


if __name__ == '__main__':
    loader = MyTestLoader()
    tests = loader.discover('tests', pattern='test_*.py')
    test_runner = MyTestRunner()
    test_runner.run(tests)
