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

import asyncio
from .connection import Connection
from .exception import ClientException


class Config:
    def __init__(self, username: str, password: str, host: str = "127.0.0.1", port: int = 2003) -> None:
        self._username = username
        self._password = password
        self._host = host
        self._port = port

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password

    def get_host(self) -> str:
        return self._host

    def get_port(self) -> int:
        return self._port

    def __hs(self) -> bytes:
        return f"H\0\0\0\0\0{len(self.get_username())}\n{len(self.get_password())}\n{self.get_username()}{self.get_password()}".encode()

    async def connect(self) -> Connection:
        """
        Establish a connection to the database instance using the set configuration.

        ## Exceptions
        Exceptions are raised in the following scenarios:
        - If the server responds with a handshake error
        - If the server sends an unknown handshake (usually caused by version incompatibility)
        """
        reader, writer = await asyncio.open_connection(self.get_host(), self.get_port())
        con = Connection(reader, writer)
        await con._write_all(self.__hs())
        resp = await con._read_exact(4)
        a, b, c, d = resp[0], resp[1], resp[2], resp[3]
        if resp == b"H\0\0\0":
            return con
        elif a == ord(b'H') and b == 0 and c == 1:
            raise ClientException(f"handshake error {d}")
        else:
            raise ClientException("unknown handshake")
