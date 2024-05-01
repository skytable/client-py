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

# NOTE: All these are just mock values and don't make any sense and often don't use correct integer boundaries

import unittest
from src.skytable_py.protocol import Protocol
from src.skytable_py.response import Value, UInt8, UInt16, UInt32, UInt64, SInt8, SInt16, SInt32, SInt64, Float32, \
    Float64, ErrorCode, Row, Empty


class ProtocolTest(unittest.TestCase):
    def test_null(self):
        self.assertEqual(Protocol(b"\x00").parse_next_element(), Value(None))

    def test_bool(self):
        self.assertEqual(
            Protocol(b"\x01\x00").parse_next_element(), Value(False))
        self.assertEqual(
            Protocol(b"\x01\x01").parse_next_element(), Value(True))

    def test_uint(self):
        self.assertEqual(
            Protocol(b"\x02255\n").parse_next_element(), Value(UInt8(255)))
        self.assertEqual(
            Protocol(b"\x03255\n").parse_next_element(), Value(UInt16(255)))
        self.assertEqual(
            Protocol(b"\x04255\n").parse_next_element(), Value(UInt32(255)))
        self.assertEqual(
            Protocol(b"\x05255\n").parse_next_element(), Value(UInt64(255)))

    def test_sint(self):
        self.assertEqual(
            Protocol(b"\x06-255\n").parse_next_element(), Value(SInt8(-255)))
        self.assertEqual(
            Protocol(b"\x07-255\n").parse_next_element(), Value(SInt16(-255)))
        self.assertEqual(
            Protocol(b"\x08-255\n").parse_next_element(), Value(SInt32(-255)))
        self.assertEqual(
            Protocol(b"\x09-255\n").parse_next_element(), Value(SInt64(-255)))

    def test_float(self):
        self.assertEqual(
            Protocol(b"\x0A3.141592654\n").parse_next_element(), Value(Float32(3.141592654)))
        self.assertEqual(
            Protocol(b"\x0B3.141592654\n").parse_next_element(), Value(Float64(3.141592654)))

    def test_binary(self):
        self.assertEqual(
            Protocol(b"\x0C6\nbinary").parse_next_element(), Value(b"binary"))

    def test_string(self):
        self.assertEqual(
            Protocol(b"\x0D6\nstring").parse_next_element(), Value("string"))

    def test_list(self):
        self.assertEqual(Protocol(b"\x0E0\n").parse_next_element(), Value([]))
        self.assertEqual(
            Protocol(
                b"\x0E5\n\x00\x01\x01\x02255\n\x06-255\n\x0A3.141592654\n").parse_next_element(),
            Value([Value(None), Value(True), Value(UInt8(255)),
                  Value(SInt8(-255)), Value(Float32(3.141592654))])
        )

    def test_error_code(self):
        self.assertEqual(
            Protocol(b"\x10\xFF\xFF").parse_next_element(), ErrorCode(65535))

    def test_row(self):
        self.assertEqual(Protocol(b"\x110\n").parse_next_element(), Row([]))
        self.assertEqual(
            Protocol(
                b"\x115\n\x00\x01\x01\x02255\n\x06-255\n\x0A3.141592654\n").parse_next_element(),
            Row([Value(None), Value(True), Value(UInt8(255)),
                 Value(SInt8(-255)), Value(Float32(3.141592654))])
        )

    def test_empty(self):
        self.assertEqual(Protocol(b"\x120\n").parse_next_element(), Empty())

    def test_rows(self):
        self.assertEqual(Protocol(b"\x130\n").parse_next_element(), [])
        self.assertEqual(
            Protocol(
                b"\x132\n5\n\x00\x01\x01\x02255\n\x06-255\n\x0A3.141592654\n1\n\x0D5\nsayan").parse_next_element(),
            [
                Row([Value(None), Value(True), Value(UInt8(255)),
                    Value(SInt8(-255)), Value(Float32(3.141592654))]),
                Row([Value("sayan")])
            ]
        )
