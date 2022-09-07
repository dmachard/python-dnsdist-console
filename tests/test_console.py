from dnsdist_console import Console
import unittest

class TestConnect(unittest.TestCase):
    def setUp(self):
        try:
            self.console = Console(host="127.0.0.1", port=5199,
                                   key="GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag=")
        except Exception as e:
            print("error connect: %s" % e)
            self.console.disconnect()
        
    def tearDown(self):
        self.console.disconnect()
        
    def test_show_version(self):
        """connect and get version"""             
        
        o = self.console.send_command(cmd="showVersion()")
        self.assertRegex(o, ".*dnsdist.*")
