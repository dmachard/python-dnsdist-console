
import re
import json

class Statistics:
    def __init__(self, console):
        """statistics class"""
        self.c = console
        
    def get_jsonstats(self):
        """Get statistics from dnsdist in JSON format"""
        # dump all stats
        o = self.c.send_command(cmd="dumpStats()")
        stats = {"global": {} }
        for l in o.splitlines():
              r = re.findall("\S+", l)
              for i in range(0, len(r), 2):
                   stats["global"][r[i]] = r[i+1]
                 
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
            
        stats["servers"] = svr_stats

        return json.dumps(stats)