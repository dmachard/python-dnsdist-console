from dnsdist_console import HashPassword
import unittest

class TestHashPassword(unittest.TestCase):
    def test_generate_hashpassword(self):
        """generate hash password"""             
        h = HashPassword().generate(password="superpassword")
        self.assertRegex(h, "^\$scrypt\$.*")