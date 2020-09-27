from dnsdist_console import Key
import unittest

class TestConnect(unittest.TestCase):
    def test_generate_key(self):
        """generate key in base64"""             
        k = Key().generate()
        self.assertRegex(k, "[a-zA-Z0-9+\/]+={0,2}")