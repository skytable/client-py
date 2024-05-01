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
from src.skytable_py.query import encode_parameter, UInt, SInt
from src.skytable_py.exception import ClientException


class TestConfig(unittest.TestCase):
    def test_encode_null(self):
        self.assertEqual(encode_parameter(None), (b"\0", 1))

    def test_encode_bool(self):
        self.assertEqual(encode_parameter(False), (b"\x010", 1))
        self.assertEqual(encode_parameter(True), (b"\x011", 1))

    def test_encode_uint(self):
        self.assertEqual(encode_parameter(UInt(1234)), (b"\x021234\n", 1))

    def test_encode_sint(self):
        self.assertEqual(encode_parameter(SInt(-1234)), (b"\x03-1234\n", 1))

    def test_encode_float(self):
        self.assertEqual(encode_parameter(3.141592654),
                         (b"\x043.141592654\n", 1))

    def test_encode_bin(self):
        self.assertEqual(encode_parameter(b"binary"), (b"\x056\nbinary", 1))

    def test_encode_str(self):
        self.assertEqual(encode_parameter("string"), (b"\x066\nstring", 1))

    def test_int_causes_exception(self):
        try:
            encode_parameter(1234)
        except ClientException as e:
            if str(e) == "unsupported type":
                pass
            else:
                self.fail(f"expected 'unsupported type' but got '{e}'")
        else:
            self.fail("expected exception but no exception was raised")
