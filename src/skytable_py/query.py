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

from abc import ABC
from typing import Tuple
# internal
from .exception import ClientException


class Query:
    def __init__(self, query: str, *argv) -> None:
        self._buffer = query.encode()
        self._param_cnt = 0
        self._q_window = len(self._buffer)
        for param in argv:
            self.add_param(param)

    def add_param(self, param: any) -> None:
        payload, param_cnt = encode_parameter(param)
        self._param_cnt += param_cnt
        self._buffer = self._buffer + payload

    def get_param_count(self) -> int:
        return self._param_cnt


class SkyhashParameter(ABC):
    def encode_self(self) -> Tuple[bytes, int]: pass


class UInt(SkyhashParameter):
    def __init__(self, v: int) -> None:
        if v < 0:
            raise ClientException("unsigned int can't be negative")
        self.v = v

    def encode_self(self) -> Tuple[bytes, int]:
        return (f"\x02{self.v}\n".encode(), 1)


class SInt(SkyhashParameter):
    def __init__(self, v: int) -> None:
        self.v = v

    def encode_self(self) -> Tuple[bytes, int]:
        return (f"\x03{self.v}\n".encode(), 1)


def encode_parameter(parameter: any) -> Tuple[bytes, int]:
    encoded = None
    if isinstance(parameter, SkyhashParameter):
        return parameter.encode_self()
    elif parameter is None:
        encoded = "\0".encode()
    elif isinstance(parameter, bool):
        encoded = f"\1{1 if parameter else 0}".encode()
    elif isinstance(parameter, float):
        encoded = f"\x04{parameter}\n".encode()
    elif isinstance(parameter, bytes):
        encoded = f"\x05{len(parameter)}\n".encode() + parameter
    elif isinstance(parameter, str):
        encoded = f"\x06{len(parameter)}\n{parameter}".encode()
    else:
        raise ClientException("unsupported type")
    return (encoded, 1)
