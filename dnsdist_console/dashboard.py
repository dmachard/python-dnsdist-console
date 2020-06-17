
from dnsdist_console import statistics

import time
import sys

class Dashboard:
    def __init__(self, console):
        """statistics class"""
        self.stats_console = statistics.Statistics(console=console)
        
    def show(self):
        """show dashboard updated every seconds"""
        prev_queries = 0
        prev_cpu_sys = 0
        prev_cpu_user = 0
                
        lines = {
                    "Uptime (seconds)": "--",
                    "Number of queries": "--",
                    "Query per second": "--",
                    "ACL drops": "--",
                    "Dynamic drops": "--",
                    "Rule drops": "--",
                    "CPU Usage": "--",
                    "Cache hitrate": "--"
                }

        sys.stdout.write("\033[1mDashboard for dnsdist\033[0m\n")
        sys.stdout.write("\n")
        for k,v in lines.items():
            sys.stdout.write("%s: %s\n" % (k,v))
        sys.stdout.write("\n")
        sys.stdout.write("Ctrl+C to exit\n")
             
        while True:
            try:
                # get stats from dnsdist
                stats = self.stats_console.get_jsonstats()
                
                qps = int(stats["queries"]) - prev_queries
                prev_queries = int(stats["queries"])
                cpu = (int(stats["cpu-sys-msec"])+int(stats["cpu-user-msec"]) - prev_cpu_sys - prev_cpu_user) / 10
                prev_cpu_sys = int(stats["cpu-sys-msec"])
                prev_cpu_user = int(stats["cpu-user-msec"])
            
                lines["Uptime (seconds)"] = stats["uptime"]
                lines["Number of queries"] = stats["queries"]
                lines["Query per second"] = qps
                lines["CPU Usage (%s)"] = cpu
                lines["ACL drops"] = stats["acl-drops"]
                lines["Rule drops"] = stats["rule-drop"]
                lines["Cache hitrate"] = stats["cache-hits"]
                lines["Dynamic drops"] = stats["dyn-blocked"]
                
                # move up cursor and delete whole line
                sys.stdout.write("\x1b[1A\x1b[2K") 
                sys.stdout.write("\x1b[1A\x1b[2K")
                for k,v in lines.items():
                    sys.stdout.write("\x1b[1A\x1b[2K") 
                sys.stdout.write("\x1b[1A\x1b[2K") 
                sys.stdout.write("\x1b[1A\x1b[2K")
                
                # reprint the lines    
                sys.stdout.write("\033[1mDashboard for dnsdist\033[0m\n")
                sys.stdout.write("\n")
                for k,v in lines.items():
                    sys.stdout.write("%s: %s\n" % (k,v))
                sys.stdout.write("\n")
                sys.stdout.write("Ctrl+C to exit\n")
        
                time.sleep(1)
            except KeyboardInterrupt:
                break