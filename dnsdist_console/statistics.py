
import re

class Statistics:
    def __init__(self, console, top_num=10):
        """statistics class"""
        self.c = console
        self.top_num = top_num
        self.__stats__ = {"global": {}, "backends": [] }
        
        self.fetch()
        
    def __repr__(self):
        """print stats"""
        return "%s" % self.__stats__
        
    def __getitem__(self, key):
        """get stats"""
        return self.__stats__[key]
        
    def fetch(self):
        """Get statistics from dnsdist"""
        
        # dump all stats
        o = self.c.send_command(cmd="dumpStats()")

        for l in o.splitlines():
              r = re.findall("\S+", l)
              for i in range(0, len(r), 2):
                   self.__stats__["global"][r[i]] = r[i+1]
                 
        # dump servers stats        
        o = self.c.send_command(cmd="showServers()")
        o_list = o.splitlines()[:-1]

        svr_hdr = o_list[0]
        
        svr_stats = []
        for s in o_list[1:]:
            svr = {}
            i = 0
            j = 0
            for i in range(len(svr_hdr)):
                if i == len(svr_hdr)-1:
                    svr[svr_hdr[j:].strip().lower()] = s[j:].strip()
                if svr_hdr[i].isupper():
                    svr[svr_hdr[j:i].strip().lower()] = s[j:i].strip()
                    j = i        
            svr_stats.append(svr)
            
        self.__stats__["backends"] = svr_stats
        
        self.__stats__["top-queries"] = self.top_queries(num=self.top_num)
        
        self.__stats__["top-nxdomain"] = self.top_nxdomain(num=self.top_num)
        
        self.__stats__["top-clients"] = self.top_clients(num=self.top_num)
        
    def top_queries(self, num=10):
        """get top queries"""
        o = self.c.send_command(cmd="topQueries(%s)" % num)
        return self.decode_top_output(o=o)
        
    def top_nxdomain(self, num=10):
        """get top non-existent domain"""
        o = self.c.send_command(cmd="topResponses(%s,DNSRCode.NXDOMAIN)" % num)
        return self.decode_top_output(o=o)
        
    def top_clients(self, num=10):
        """get top clients"""
        o = self.c.send_command(cmd="topClients(%s)" % num)
        return self.decode_top_output(o=o)
        
    def decode_top_output(self, o):
        """decode top output"""
        o_list = []
        for l in o.splitlines()[:-1]:
            r = re.findall("\S+", l)
            o_list.append({"entry": r[1], "hits": r[2]})
        return o_list