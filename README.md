# Skytable Python Client

![PyPI - Version](https://img.shields.io/pypi/v/skytable-py) ![Static Badge](https://img.shields.io/badge/python-%3E%3D3.9-blue) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/skytable/client-py/test.yml) ![GitHub License](https://img.shields.io/github/license/skytable/client-py)

This is the official Python client driver for [Skytable](https://github.com/skytable/skytable). The driver has been tested to work with [Skytable 0.8.2](https://github.com/skytable/skytable/releases/tag/v0.8.2) using the [Skyhash/2 Protocol](https://docs.skytable.io/protocol/). The Python client driver provides first-class `async` support using `asyncio` and does not have any additional dependencies at the moment.

## Example usage

Install the dependency:

```sh
pip install skytable-py
```

Use in your code:
```python
import asyncio
from skytable_py import Config, Query


c = Config("root", "mypassword123456789")


async def main():
    db = None
    try:
        db = await c.connect()
        # init space
        assert (await db.run_simple_query(Query("create space apps"))).is_empty()
        # init model
        assert (await db.run_simple_query(Query("create model apps.auth(username: string, password: string)"))).is_empty()
        # insert our test row
        assert (await db.run_simple_query(Query("insert into apps.auth(?, ?)", "sayan", "mypassword"))).is_empty()
        # fetch data
        username, password = (await db.run_simple_query(Query("select * from apps.auth where username = ?", "sayan"))).row().columns
        # output
        print(f"username={username.string()}, password={password.string()}")
    except Exception as e:
        print(f"failed with error {e}")
    finally:
        if db:
            await db.close()

if __name__ == "__main__":
    asyncio.run(main())

```

## License

This client library is distributed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
