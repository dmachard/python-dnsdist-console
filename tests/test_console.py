from dnsdist_console import Console
import unittest

class TestConnect(unittest.TestCase):
    def setUp(self):
        self.console = Console(host="127.0.0.1", port=5199,
                               key="GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag=")
        
    def tearDown(self):
        self.console.disconnect()
        
    def test_show_version(self):
        """connect and get version"""             
        
        o = self.console.send_command(cmd="showVersion()")
        self.assertRegex(o, ".*dnsdist.*")


class TestConnectV6(unittest.TestCase):
    def setUp(self):
        self.console = Console(host="::1", port=5199,
                               key="GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag=")

    def tearDown(self):
        self.console.disconnect()

    def test_show_version(self):
        """connect and get version"""

        o = self.console.send_command(cmd="showVersion()")
        self.assertRegex(o, ".*dnsdist.*")
