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

from asyncio import StreamReader, StreamWriter
from .query import Query
from .exception import ProtocolException


class Connection:
    """
    A database connection to a Skytable instance
    """

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        self._reader = reader
        self._writer = writer
        self._cursor = 0
        self.buffer = bytes()

    async def _write_all(self, bytes: bytes):
        self._write(bytes)
        await self._flush()

    def _write(self, bytes: bytes) -> None:
        self._writer.write(bytes)

    def __buffer(self) -> bytes:
        return self.buffer[:self._cursor]

    async def _flush(self):
        await self._writer.drain()

    async def _read_exact(self, count) -> bytes:
        return await self._reader.readexactly(count)

    async def close(self):
        """
        Close this connection
        """
        self._writer.close()
        await self._writer.wait_closed()

    def __parse_string(self) -> None | str:
        strlen = self.__parse_int()
        if strlen:
            if len(self.__buffer()) >= strlen:
                strlen = self.__buffer()[:strlen].decode()
                self._cursor += strlen
                return strlen

    def __parse_binary(self) -> None | bytes:
        binlen = self.__parse_int()
        if binlen:
            if len(self.__buffer()) >= binlen:
                binlen = self.__buffer()[:binlen].decode()
                self._cursor += binlen
                return binlen

    def __parse_int(self) -> None | int:
        i = 0
        strlen = 0
        stop = False
        buffer = self.__buffer()

        while i < len(buffer) and not stop:
            digit = None
            if 48 <= buffer[i] <= 57:
                digit = buffer[i] - 48

            if digit is not None:
                strlen = (10 * strlen) + digit
                i += 1
            else:
                raise ProtocolException("invalid response from server")

            if i < len(buffer) and buffer[i] == ord(b'\n'):
                stop = True
                i += 1

        if stop:
            self._cursor += i
            self._cursor += 1  # for LF
            return strlen

    async def run_simple_query(self, query: Query):
        query_window_str = str(len(query._q_window))
        total_packet_size = len(query_window_str) + 1 + len(query._buffer)
        # write metaframe
        metaframe = f"S{str(total_packet_size)}\n{query_window_str}\n"
        await self._write_all(metaframe.encode())
        # write dataframe
        await self._write_all(query._buffer)
        # now enter read loop
        while True:
            read = await self._reader.read(1024)
            if len(read) == 0:
                raise ConnectionResetError
            self.buffer = self.buffer + read
