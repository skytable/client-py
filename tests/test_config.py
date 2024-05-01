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
from src.skytable_py import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.c = Config("root", "mypassword123456789")

    def test_username(self):
        self.assertEqual(self.c.get_username(), "root")

    def test_password(self):
        self.assertEqual(self.c.get_password(), "mypassword123456789")

    def test_host(self):
        self.assertEqual(self.c.get_host(), "127.0.0.1")

    def test_port(self):
        self.assertEqual(self.c.get_port(), 2003)


if __name__ == '__main__':
    unittest.main()
