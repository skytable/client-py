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

from typing import Union, List
from .exception import ProtocolException
from .response import Value, UInt8, UInt16, UInt32, UInt64, SInt8, SInt16, SInt32, SInt64, Float32, Float64, Empty, \
    ErrorCode, Row, Response


class Protocol:
    def __init__(self, buffer=bytes()) -> None:
        self._buffer = buffer
        self._cursor = 0

    def push_additional_bytes(self, additional_bytes: bytes) -> None:
        self._buffer = self._buffer + additional_bytes

    def __step(self) -> int:
        ret = self.__buf()[0]
        self.__increment_cursor()
        return ret

    def __decrement(self) -> None:
        self._cursor -= 1

    def __increment_cursor_by(self, by: int) -> None:
        self._cursor += by

    def __increment_cursor(self) -> None:
        self.__increment_cursor_by(1)

    def __buf(self) -> bytes:
        return self._buffer[self._cursor:]

    def __remaining(self) -> int:
        return len(self.__buf())

    def __is_eof(self) -> bool:
        return self.__remaining() == 0

    def parse_next_int(self, stop_symbol='\n') -> Union[None, int]:
        i = 0
        integer = 0
        stop = False
        buffer = self.__buf()

        while i < len(buffer) and not stop:
            digit = None
            if 48 <= buffer[i] <= 57:
                digit = buffer[i] - 48

            if digit is not None:
                integer = (10 * integer) + digit
                i += 1
            else:
                raise ProtocolException("invalid response from server")

            if i < len(buffer) and buffer[i] == ord(stop_symbol):
                stop = True

        if stop:
            self.__increment_cursor_by(i)
            self.__increment_cursor()  # for LF
            return integer

    def parse_next_string(self) -> Union[None, Value]:
        strlen = self.parse_next_int()
        if strlen:
            if self.__remaining() >= strlen:
                string = self.__buf()[:strlen].decode()
                self.__increment_cursor_by(strlen)
                return Value(string)

    def parse_next_binary(self) -> Union[None, Value]:
        binlen = self.parse_next_int()
        if binlen:
            if self.__remaining() >= binlen:
                blob = self.__buf()[:binlen]
                self.__increment_cursor_by(binlen)
                return Value(blob)

    def parse_boolean(self) -> Union[None, Value]:
        # boolean
        if self.__is_eof():
            self.__decrement()  # move back to type symbol
            return None
        else:
            byte = self.__step()
            if byte > 1:
                raise ProtocolException("received invalid data")
            return Value(True) if byte == 1 else Value(False)

    def parse_uint(self, type_symbol: int) -> Union[None, Value]:
        # uint
        integer = self.parse_next_int()
        if integer:
            if type_symbol == 2:
                return Value(UInt8(integer))
            elif type_symbol == 3:
                return Value(UInt16(integer))
            elif type_symbol == 4:
                return Value(UInt32(integer))
            else:
                return Value(UInt64(integer))
        else:
            self.__decrement()  # move back to type symbol

    def parse_sint(self, type_symbol: int) -> Union[None, Value]:
        # sint
        if self.__is_eof():
            self.__decrement()  # move back to type symbol
            return None
        is_negative = False
        if self.__step() == ord('-'):
            is_negative = True
        else:
            self.__decrement()  # move back to integer starting position since there is no '-'
        integer = self.parse_next_int()
        if integer:
            if is_negative:
                integer = -integer
            if type_symbol == 6:
                return Value(SInt8(integer))
            elif type_symbol == 7:
                return Value(SInt16(integer))
            elif type_symbol == 8:
                return Value(SInt32(integer))
            else:
                return Value(SInt64(integer))
        else:
            self.__decrement()  # move back to type symbol
            if is_negative:
                self.__decrement()  # move back to starting position of this integer

    def parse_float(self, type_symbol: int) -> Union[None, Value]:
        if self.__is_eof():
            self.__decrement()  # move back to type symbol
            return None
        is_negative = False
        if self.__step() == ord('-'):
            is_negative = True
        else:
            self.__decrement()  # move back to float starting position since there is no '-'
        whole = self.parse_next_int(stop_symbol='.')
        if whole:
            decimal = self.parse_next_int()
            if decimal:
                full_float = float(f"{whole}.{decimal}")
                if is_negative:
                    full_float = -full_float
                if type_symbol == 10:
                    return Value(Float32(full_float))
                else:
                    return Value(Float64(full_float))
        self.__decrement()  # type symbol
        if is_negative:
            self.__decrement()

    def parse_error_code(self) -> Union[None, ErrorCode]:
        if self.__remaining() < 2:
            self.__decrement()  # type symbol
        else:
            a, b = self.__buf()
            self.__increment_cursor_by(2)
            return ErrorCode(int.from_bytes([a, b], byteorder="little", signed=False))

    def parse_list(self) -> Union[None, Value]:
        cursor_start = self._cursor - 1
        list_len = self.parse_next_int()
        if list_len is None:
            self.__decrement()  # type symbol
            return None
        items = []
        while len(items) != list_len:
            element = self.parse_next_element()
            if element:
                items.append(element)
            else:
                self._cursor = cursor_start
                return None
        return Value(items)

    def parse_row(self) -> Union[None, Row]:
        cursor_start = self._cursor - 1
        column_count = self.parse_next_int()
        if column_count is None:
            self.__decrement()  # type symbol
            return None
        columns = []
        while len(columns) != column_count:
            column = self.parse_next_element()
            if column:
                columns.append(column)
            else:
                self._cursor = cursor_start
                return None
        return Row(columns)

    def parse_rows(self) -> Union[None, List[Row]]:
        cursor_start = self._cursor - 1
        row_count = self.parse_next_int()
        rows = []
        while len(rows) != row_count:
            row = self.parse_row()
            if row:
                rows.append(row)
            else:
                self._cursor = cursor_start
                return None
        return rows

    def parse(self) -> Response:
        e = self.parse_next_element()
        if e:
            return Response(e)

    def parse_next_element(self) -> Union[None, Value, Empty, ErrorCode]:
        if self.__is_eof():
            return None
        type_symbol = self.__step()
        if type_symbol == 0:
            # null
            return Value(None)
        elif type_symbol == 1:
            return self.parse_boolean()
        elif 2 <= type_symbol <= 5:
            return self.parse_uint(type_symbol)
        elif 6 <= type_symbol <= 9:
            return self.parse_sint(type_symbol)
        elif 10 <= type_symbol <= 11:
            return self.parse_float(type_symbol)
        elif type_symbol == 12:
            return self.parse_next_binary()
        elif type_symbol == 13:
            return self.parse_next_string()
        elif type_symbol == 14:
            return self.parse_list()
        elif type_symbol == 15:
            raise ProtocolException("dictionaries are not supported yet")
        elif type_symbol == 16:
            return self.parse_error_code()
        elif type_symbol == 17:
            return self.parse_row()
        elif type_symbol == 18:
            return Empty()
        elif type_symbol == 19:
            return self.parse_rows()
        else:
            raise ProtocolException(
                f"unknown type with code {type_symbol} sent by server")
