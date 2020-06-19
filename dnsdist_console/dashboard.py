
from dnsdist_console import statistics

import time
import sys
import json

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
                    "CPU Usage (%s)": "--",
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
                stats_json = json.loads(stats)
                global_stats = stats_json["global"]
                
                qps = int(global_stats["queries"]) - prev_queries
                prev_queries = int(global_stats["queries"])
                cpu = (int(global_stats["cpu-sys-msec"])+int(global_stats["cpu-user-msec"]) - prev_cpu_sys - prev_cpu_user) / 10
                prev_cpu_sys = int(global_stats["cpu-sys-msec"])
                prev_cpu_user = int(global_stats["cpu-user-msec"])
            
                lines["Uptime (seconds)"] = global_stats["uptime"]
                lines["Number of queries"] = global_stats["queries"]
                lines["Query per second"] = qps
                lines["CPU Usage (%s)"] = cpu
                lines["ACL drops"] = global_stats["acl-drops"]
                lines["Rule drops"] = global_stats["rule-drop"]
                lines["Cache hitrate"] = global_stats["cache-hits"]
                lines["Dynamic drops"] = global_stats["dyn-blocked"]
                
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