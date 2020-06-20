
import re

class Statistics:
    def __init__(self, console):
        """statistics class"""
        self.c = console
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