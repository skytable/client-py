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

from dataclasses import dataclass
from typing import Union, List
from .exception import ClientException


@dataclass
class UInt8:
    inner: int


@dataclass
class UInt16:
    inner: int


@dataclass
class UInt32:
    inner: int


@dataclass
class UInt64:
    inner: int


@dataclass
class SInt8:
    inner: int


@dataclass
class SInt16:
    inner: int


@dataclass
class SInt32:
    inner: int


@dataclass
class SInt64:
    inner: int


@dataclass
class Float32:
    inner: float


@dataclass
class Float64:
    inner: float


class Empty:
    pass

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Empty):
            return True
        return False


class Value:
    def __init__(self, value: Union[None, bool, UInt8, UInt16, UInt32, UInt64,
                                    SInt8, SInt16, SInt32, SInt64,
                                    Float32, Float64, bytes, str, list]):
        self.repr = value

    def is_null(self) -> bool:
        return self.repr is None

    def data(self) -> Union[None, bool, int, float, bytes, str, list]:
        if self.repr is None:
            return None
        elif isinstance(self.repr, (UInt8, UInt16, UInt32, UInt64, SInt8, SInt16, SInt32, SInt64)):
            return self.repr.inner
        elif isinstance(self.repr, (Float32, Float64)):
            return self.repr.inner
        elif isinstance(self.repr, str):
            return self.repr
        elif isinstance(self.repr, bytes):
            return self.repr
        elif isinstance(self.repr, list):
            return self.repr
        elif isinstance(self.repr, bool):
            return self.repr
        else:
            raise ClientException("unknown type")

    def int(self) -> Union[None, int]:
        if isinstance(self.repr, (UInt8, UInt16, UInt32, UInt64, SInt8, SInt16, SInt32, SInt64)):
            return self.repr.inner
        return None

    def float(self) -> Union[None, float]:
        if isinstance(self.repr, (Float32, Float64)):
            return self.repr.inner
        return None

    def string(self) -> Union[None, str]:
        if isinstance(self.repr, str):
            return self.repr
        return None

    def binary(self) -> Union[None, bytes]:
        if isinstance(self.repr, bytes):
            return self.repr
        return None

    def list(self) -> Union[None, list]:
        if isinstance(self.repr, list):
            return self.repr
        return None

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.data() == other.data()
        return False


class Row:
    def __init__(self, values: List[Value]) -> None:
        self.columns = values

    def __eq__(self, other):
        if isinstance(other, Row):
            return self.columns == other.columns
        return False


@dataclass
class ErrorCode:
    inner: int


class Response:
    def __init__(self, resp: Union[Empty, Value, Row, List[Row], ErrorCode]):
        self.data = resp

    def is_empty(self) -> bool:
        return isinstance(self.data, Empty)

    def value(self) -> Union[None, Value]:
        if isinstance(self.data, Value):
            return self.data

    def row(self) -> Union[None, Row]:
        if isinstance(self.data, Row):
            return self.data

    def rows(self) -> Union[None, List[Row]]:
        if isinstance(self.data, list):
            return self.data

    def error(self) -> Union[None, int]:
        if isinstance(self.data, ErrorCode):
            return self.data.inner
