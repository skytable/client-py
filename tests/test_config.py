import unittest
from src.skytable_py import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.c = Config("root", "mypassword123456789")

    def test_username(self):
        self.assertEqual(self.c.get_username(), "root")

    def test_password(self):
        self.assertEqual(self.c.get_password(), "mypassword123456789")

    def test_host(self):
        self.assertEqual(self.c.get_host(), "127.0.0.1")

    def test_port(self):
        self.assertEqual(self.c.get_port(), 2003)


if __name__ == '__main__':
    unittest.main()
