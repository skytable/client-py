import asyncio
from asyncio import StreamReader, StreamWriter


class ClientException(Exception):
    """
    An exception thrown by this client library
    """
    pass


class Connection:
    """
    A database connection to a Skytable instance
    """

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        self._reader = reader
        self._writer = writer

    async def _write_all(self, bytes: bytes):
        self._write(bytes)
        await self._flush()

    def _write(self, bytes: bytes) -> None:
        self._writer.write(bytes)

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
