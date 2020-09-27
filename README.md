# Python client for dnsdist console

You can use it to execute remote commands, display a dashboard or easily extract statistics.

![Build](https://github.com/dmachard/dnsdist-console/workflows/Build/badge.svg) ![Testing](https://github.com/dmachard/dnsdist-console/workflows/Testing/badge.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI](https://github.com/dmachard/dnsdist-console/workflows/Publish%20to%20PyPI/badge.svg)


## Table of contents
* [Installation](#installation)
* [Generate key](#generate-key)
* [Run command](#run-command)
* [Get statistics](#get-statistics)
* [Display basic dashboard](#display-basic-dashboard)

## Installation

This module can be installed from [pypi](https://pypi.org/project/dnsdist_console/) website

```python
pip install dnsdist_console
```

## Generate key

You must configure your dnsdist load balancer to accept remote connection to the console.
This module can be used to generate the secret key as below.

The command in one line 

```bash
python3 -c "from dnsdist_console import Key;print(Key().generate())"
OTgmgAR6zbrfrYlKgsAAJn+by4faMqI1bVCvzacXMW0=
```

Save-it in your `/etc/dnsdist/dnsdist.conf` with the `setKey` directive.

```
controlSocket('0.0.0.0:5199')
setKey("GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag=")
```

## Run command

Configure the client with the IP address and the TCP port of your dnsdist as well as the associated secret key. If the provided key is incorrect, an exception will be raised.

```python
from dnsdist_console import Console

console_ip = "127.0.0.1"
console_port = 5199
console_key = "GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag="

console = Console(host=console_ip,
                  port=console_port, 
                  key=console_key)
```

Please refer to the [dnsdist documentation](https://dnsdist.org/reference/config.html) for all available commands.

```python
o = console.send_command(cmd="showVersion()")
print(o)
dnsdist 1.4.0

```

## Get statistics

Use this module to extract some statistics on your dnsdist load balancer.
Statistics are stored in a python dictionary.

```python
from dnsdist_console import Statistics

s = Statistics(console=console)
print(s["global"]["queries"])
3993

# get top queries
print(s["top-queries"])
[
    {'entry': 'www.apple.com.', 'hits': '9'},
    {'entry': 'www.facebook.com.', 'hits': '3'},
    {'entry': 'www.microsoft.com.', 'hits': '3'}
]


# get top nx domain
print(s["top-nxdomain"])
[
    {'entry': 'www.nxdomain.com.', 'hits': '1'}
    
]

# get top clients
print(s["top-clients"])
[
    {'entry': '127.0.0.1', 'hits': '21'}
]
```

Statistics available:

- globals (dict):
    - acl-drops: Number of packets dropped because of the ACL
    - latency-avg100: Average response latency in microseconds of the last 100 packets
    - latency-avg1000: Average response latency in microseconds of the last 1000 packets
    - latency-avg10000: Average response latency in microseconds of the last 10000 packets
    - latency-avg1000000: Average response latency in microseconds of the last 1000000 packets
    - latency0-1: Number of queries answered in less than 1ms
    - latency1-10: Number of queries answered in 1-10 ms
    - latency10-50: Number of queries answered in 10-50 ms
    - latency50-100: Number of queries answered in 50-100 ms
    - latency100-1000: Number of queries answered in 100-1000 ms
    - cache-hits: Number of times an answer was retrieved from cache
    - cache-misses: Number of times an answer not found in the cache
    - cpu-sys-msec: Milliseconds spent by dnsdist in the system state
    - cpu-user-msec: Milliseconds spent by dnsdist in the user state
    - downstream-send-errors: Number of errors when sending a query to a backend
    - no-policy: Number of queries dropped because no server was available
    - downstream-timeouts: Number of queries not answered in time by a backend
    - noncompliant-queries: Number of queries dropped as non-compliant
    - dyn-block-nmg-size: Number of dynamic blocks entries
    - noncompliant-responses: Number of answers from a backend dropped as non-compliant
    - dyn-blocked: Number of queries dropped because of a dynamic block
    - queries: Number of received queries
    - empty-queries: Number of empty queries received from clients
    - rdqueries: Number of received queries with the recursion desired bit set
    - fd-usage: Number of currently used file descriptors
    - real-memory-usage: Current memory usage in bytes
    - frontend-noerror: "Number of NoError answers sent to clients
    - responses: Number of responses received from backends
    - frontend-nxdomain: Number of NXDomain answers sent to clients
    - rule-drop: Number of queries dropped because of a rule"
    - frontend-servfail: Number of SERVFAIL answers sent to clients
    - rule-nxdomain: Number of NXDomain answers returned because of a rule
    - rule-refused: Number of Refused answers returned because of a rule
    - rule-servfail: Number of SERVFAIL answers received because of a rule
    - security-status: Security status of this software. 0=unknown, 1=OK, 2=upgrade recommended, 3=upgrade mandatory
    - self-answered: Number of self-answered responses
    - latency-count: Number of queries contributing to response time histogram
    - servfail-responses: Number of SERVFAIL answers received from backends
    - latency-slow: Number of queries answered in more than 1 second
    - special-memory-usage: Memory usage (more precise)
    - latency-sum: Total response time of all queries combined in milliseconds since the start of dnsdist
    - trunc-failures: Number of errors encountered while truncating an answer
    - uptime: Uptime of the dnsdist process in seconds

- backends (list):
    - \#: The number of the server
    - name: The name associated to this backend
    - address: The IP address and port of the server
    - state: backend is up or down
    - qps: Current number of queries per second
    - qlim: Maximum number of queries per second
    - ord: The order in which this server is picked
    - wt: The weight within the order in which this server is picked
    - queries: Amount of queries relayed to server
    - drops: Amount of queries not answered by serve
    - drate: Number of queries dropped per second by this server
    - lat: Server's latency when answering questions in milliseconds
    - outstanding: Current number of queries that are waiting for a backend response
    - pools: The pools this server belongs to

- top-queries (list):
    - entry: domain name
    - hits: number of hit
    
- top-nxdomain (list):
    - entry: non-existent domain name
    - hits: number of hit
    
- top-clients (list):
    - entry: client ip address
    - hits: number of hit
    
## Display basic dashboard

You can use this client to display a dashboard of your dnsdist from your command line.
The dashboard is updated every second.

```python
from dnsdist_console import Dashboard

Dashboard(console=console)
```

Run your script and you will see something like below.

```bash
Dashboard for dnsdist

Global:
        Uptime (seconds): 47735
        Number of queries: 0
        Query per second: 0
        ACL drops: 0
        Dynamic drops: 0
        Rule drops: 0
        CPU Usage (%s): 2.8
        Cache hitrate: 0
Backends:
        #0 / 10.0.0.140:53 / -- / dns_others
                Number of queries: 0
                Query per second: 0.0
                Number of drops: 0
        #1 / 10.0.0.55:53 / -- / dns_internal
                Number of queries: 0
                Query per second: 0.0
                Number of drops: 0
        #2 / 8.8.8.8:53 / -- / dns_internet
                Number of queries: 0
                Query per second: 0.0
                Number of drops: 0
        #3 / 1.1.1.1:53 / dns_1 / --
                Number of queries: 0
                Query per second: 0.0
                Number of drops: 0

Ctrl+C to exit
```