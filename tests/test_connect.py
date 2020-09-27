from dnsdist_console import Console
import unittest

class TestConnect(unittest.TestCase):
    def test_show_version(self):
        """connect and get version"""             
        console = Console(host="127.0.0.1", port=5199,
                          key="GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag=")
        o = console.send_command(cmd="showVersion()")
        self.assertRegex(o, ".*dnsdist.*")
