# Skytable Python Client

This is an alpha version of Skytable's official connector for Python 3.X.

## Example

```python
import asyncio
from skytable_py import Config

c = Config(username="root", password="password")


async def main():
    db = await c.connect()
    # ... use the db


if __name__ == "__main__":
    asyncio.run(main())

```

## License

This client library is distributed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
