from dnsdist_console import Console
from dnsdist_console import Statistics

# dnsdist console
console_ip = "10.0.0.27"
console_port = 5199
console_key = "OTgmgAR6zbrfrYlKgsAAJn+by4faMqI1bVCvzacXMW0="

# do hanshake
c = Console(host=console_ip, port=console_port, key=console_key)

# get global stats
s = Statistics(console=c)
print(s["global"]["queries"])

# get top queries
print(s["top-queries"])

# get top nx domain
print(s["top-nxdomain"])

# get top clients
print(s["top-clients"])