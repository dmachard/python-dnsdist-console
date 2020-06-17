
import re

class Statistics:
    def __init__(self, console):
        """statistics class"""
        self.console = console
        
    def get_jsonstats(self):
        """Get statistics from dnsdist in JSON format"""
        o = self.console.send_command(cmd="dumpStats()")
        stats = {}
        for l in o.splitlines():
              r = re.findall("\S+", l)
              for i in range(0, len(r), 2):
                   stats[r[i]] = r[i+1]
        return stats