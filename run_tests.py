# Copyright 2024, Sayan Nandan <nandansayan@outlook.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

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
