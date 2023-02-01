from dnsdist_console import Console
from dnsdist_console import Statistics
import unittest

import dns.resolver

                           
my_resolver = dns.resolver.Resolver(configure=False)
my_resolver.nameservers = ['127.0.0.1']
my_resolver.port = 5553

r = my_resolver.resolve('www.github.com', 'a')
try:
    r = my_resolver.resolve('12345678', 'a')
except dns.resolver.NXDOMAIN:
    pass

class TestStatistic(unittest.TestCase):
    def setUp(self):
        self.console = Console(host="127.0.0.1", port=5199,
                               key="GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag=")

    def tearDown(self):
        self.console.disconnect()
        
    def test_get_global(self):
        """get global stats"""
        s = Statistics(console=self.console)

        print(s["global"])

        self.assertGreater(int(s["global"]["queries"]), 2)

    def test_get_topqueries(self):
        """get top queries"""
        s = Statistics(console=self.console)

        print(s["top-queries"])

        self.assertEqual(len(s["top-queries"]), 2)
        self.assertGreater(int(s["top-queries"][0]["hits"]), 0)

    def test_get_nxdomain(self):
        """get nxdomain"""
        s = Statistics(console=self.console)

        print(s["top-nxdomain"])

        self.assertEqual(len(s["top-nxdomain"]), 1)
        self.assertGreater(int(s["top-nxdomain"][0]["hits"]), 0)

    def test_get_topclients(self):
        """get top clients"""
        s = Statistics(console=self.console)

        print(s["top-clients"])

        self.assertEqual(len(s["top-clients"]), 1)
        self.assertGreater(int(s["top-clients"][0]["hits"]), 0)

    def test_backends(self):
        """backends"""
        s = Statistics(console=self.console)

        # 4 backends ?
        self.assertEqual(len(s["backends"]), 4)

        tc = { 
                "0": {'Name': 'a long name with spa', 'Pools': 'a pool with spaces'},
                "1": {'Name': 'name with spaces', 'Pools': 'apoolwithoutspaces'},
                "2": {'Name': 'namewithoutspaces', 'Pools': 'shortpool'},
                "3":  {'Name': 'and a long long long', 'Pools': 'a long long long long pool'}
            }
        for b in s["backends"]:
            if b["#"] in tc:
                self.assertEqual(b["Name"], tc[b["#"]]["Name"])
                self.assertEqual(b["Pools"], tc[b["#"]]["Pools"])