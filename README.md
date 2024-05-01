# Skytable Python Client

> **Note**: This library is currently in alpha

This is an alpha version of Skytable's official connector for Python 3.X.


## Example

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
