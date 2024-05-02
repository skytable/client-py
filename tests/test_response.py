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
from src.skytable_py.protocol import Protocol
from src.skytable_py.response import Response, Value, UInt8, UInt16, UInt32, UInt64, SInt8, SInt16, SInt32, SInt64, Float32, Float64, ErrorCode, Row, Empty


class ProtocolTest(unittest.TestCase):
    def test_integer_decode(self):
        self.assertEqual(Protocol(b"12345678\n").parse_next_int(), 12345678)

    def test_string_decode(self):
        blob = b"11\nhello world"
        for i in range(0, len(blob)):
            self.assertEqual(
                Protocol(blob[:i]).parse_next_string(), None)
        self.assertEqual(
            Protocol(blob).parse_next_string().data(), "hello world")

    def test_binary_decode(self):
        blob = b"11\nhello world"
        for i in range(0, len(blob)):
            self.assertEqual(
                Protocol(blob[:i]).parse_next_binary(), None)
        self.assertEqual(
            Protocol(blob).parse_next_binary().data(), b"hello world")

    def test_response_types(self):
        # null
        self.assertTrue(Response(Value(None)).value().is_null())
        # bool
        self.assertEquals(Response(Value(True)).value().repr, True)
        self.assertEquals(Response(Value(False)).value().repr, False)
        # uint
        self.assertEquals(Response(Value(UInt8(255))).value().repr.inner, 255)
        self.assertEquals(Response(Value(UInt16(255))).value().repr.inner, 255)
        self.assertEquals(Response(Value(UInt32(255))).value().repr.inner, 255)
        self.assertEquals(Response(Value(UInt64(255))).value().repr.inner, 255)
        # sint
        self.assertEquals(Response(Value(SInt8(-1))).value().repr.inner, -1)
        self.assertEquals(Response(Value(SInt16(-1))).value().repr.inner, -1)
        self.assertEquals(Response(Value(SInt32(-1))).value().repr.inner, -1)
        self.assertEquals(Response(Value(SInt64(-1))).value().repr.inner, -1)
        # float
        self.assertEquals(Response(Value(Float32(3.141592654))
                                   ).value().repr.inner, 3.141592654)
        self.assertEquals(Response(Value(Float64(3.141592654))
                                   ).value().repr.inner, 3.141592654)
        self.assertEquals(Response(Value(Float32(-3.141592654))
                                   ).value().repr.inner, -3.141592654)
        self.assertEquals(Response(Value(Float64(-3.141592654))
                                   ).value().repr.inner, -3.141592654)
        # simple collections
        self.assertEquals(Response(Value(b"bytes")).value().repr, b"bytes")
        self.assertEquals(Response(Value("string")).value().repr, "string")
        # complex collections
        self.assertEquals(Response(Value([Value(b"bytes"), Value("string")])).value(
        ).repr, [Value(b"bytes"), Value("string")])
        # server error
        self.assertEquals(Response(ErrorCode(132)).error(), 132)
        # row
        self.assertEquals(Response(Row([Value("hello"), Value(b"world")])).row(
        ).columns, [Value("hello"), Value(b"world")])
        # empty
        self.assertTrue(Response(Empty()).is_empty())
        # multi row
        self.assertEquals(Response([Row([Value("sayan"), Value(b"cakes")]), Row(
            [Value("sophie"), Value(b"cookies")])]).rows(), [Row([Value("sayan"), Value(b"cakes")]), Row(
                [Value("sophie"), Value(b"cookies")])])
