# Python client for dnsdist console

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dnsdist-console)
![](https://github.com/dmachard/dnsdist_console/workflows/Publish%20to%20PyPI/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

| | |
| ------------- | ------------- |
| Author |  Denis Machard <d.machard@gmail.com> |
| License |  MIT | 
| PyPI |  https://pypi.org/project/dnsdist_console/ |
| | |

This is a Python 3 client for the dnsdist console

## Table of contents
* [Installation](#installation)
* [Generate key](#generate-key)
* [Handshake](#handshake)
* [Run command](#run-command)
* [Get statistics](#get-statistics)
* [Display dashboard](#display-dashboard)

## Installation

```python
pip install dnsdist_console
```

## Generate key

Generate a shared secret key.
It will be used between the client and the server.

```python
from dnsdist_console import Key

k = Key().generate()
print(k)
OTgmgAR6zbrfrYlKgsAAJn+by4faMqI1bVCvzacXMW0=
```

The command in one line 

```bash
python3 -c "from dnsdist_console import Key;print(Key().generate())"
```

Save-it in your `/etc/dnsdist/dnsdist.conf` with the `setKey` directive.

```
controlSocket('0.0.0.0:5199')
setKey("GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag=")
```

## Handshake

```python
from dnsdist_console import Console

console_ip = "127.0.0.1"
console_port = 5199
console_key = "GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag="

console = Console(host=console_ip,
                  port=console_port, 
                  key=console_key)
```

## Run command

Please refer to the dnsdist documentation for available commands.

```python
o = console.send_command(cmd="showVersion()")
print(o)
dnsdist 1.4.0

```

## Get statistics

Get statistics from dnsdist in JSON format. 

```python
from dnsdist_console import Console
from dnsdist_console import Statistics

# dnsdist console
console_ip = "10.0.0.27"
console_port = 5199
console_key = "OTgmgAR6zbrfrYlKgsAAJn+by4faMqI1bVCvzacXMW0="

c = Console(host=console_ip, port=console_port, key=console_key)
s = Statistics(console=c)
                  
stats = s.get_jsonstats()
print(stats)
```

JSON output example

```json
{
  "global": {
    "acl-drops": "0",
    "latency0-1": "0",
    "cache-hits": "0",
    "latency1-10": "0",
    "cache-misses": "0",
    "latency10-50": "0",
    "cpu-sys-msec": "6010",
    "latency100-1000": "0",
    "cpu-user-msec": "39325",
    "latency50-100": "0",
    "downstream-send-errors": "0",
    "no-policy": "0",
    "downstream-timeouts": "0",
    "noncompliant-queries": "0",
    "dyn-block-nmg-size": "0",
    "noncompliant-responses": "0",
    "dyn-blocked": "0",
    "queries": "0",
    "empty-queries": "0",
    "rdqueries": "0",
    "fd-usage": "24",
    "real-memory-usage": "1140137984",
    "frontend-noerror": "0",
    "responses": "0",
    "frontend-nxdomain": "0",
    "rule-drop": "0",
    "frontend-servfail": "0",
    "rule-nxdomain": "0",
    "latency-avg100": "0.0",
    "rule-refused": "0",
    "latency-avg1000": "0.0",
    "rule-servfail": "0",
    "latency-avg10000": "0.0",
    "security-status": "0",
    "latency-avg1000000": "0.0",
    "self-answered": "0",
    "latency-count": "0",
    "servfail-responses": "0",
    "latency-slow": "0",
    "special-memory-usage": "84602880",
    "latency-sum": "0",
    "trunc-failures": "0",
    "uptime": "9973"
  },
  "servers": [
    {
      "#": "0",
      "name": "",
      "address": "10.0.0.140:53",
      "state": "UP",
      "qps": "0.0",
      "qlim": "0",
      "ord": "1",
      "wt": "1",
      "queries": "0",
      "drops": "0",
      "drate": "0.0",
      "lat": "0.0",
      "outstanding": "0",
      "pools": "dns_other"
    },
    {
      "#": "1",
      "name": "",
      "address": "10.0.0.55:53",
      "state": "UP",
      "qps": "0.0",
      "qlim": "0",
      "ord": "1",
      "wt": "1",
      "queries": "0",
      "drops": "0",
      "drate": "0.0",
      "lat": "0.0",
      "outstanding": "0",
      "pools": "dns_internal"
    },
    {
      "#": "2",
      "name": "",
      "address": "8.8.8.8:53",
      "state": "UP",
      "qps": "0.0",
      "qlim": "0",
      "ord": "1",
      "wt": "1",
      "queries": "0",
      "drops": "0",
      "drate": "0.0",
      "lat": "0.0",
      "outstanding": "0",
      "pools": "dns_internet"
    },
    {
      "#": "3",
      "name": "dns1",
      "address": "1.1.1.1:53",
      "state": "up",
      "qps": "0.0",
      "qlim": "0",
      "ord": "1",
      "wt": "1",
      "queries": "0",
      "drops": "0",
      "drate": "0.0",
      "lat": "0.0",
      "outstanding": "0",
      "pools": ""
    }
  ]
}
```

## Display dashboard

Display dashboard for dnsdist from command line

```python
from dnsdist_console import Console
from dnsdist_console import Dashboard

# dnsdist console
console_ip = "10.0.0.27"
console_port = 5199
console_key = "OTgmgAR6zbrfrYlKgsAAJn+by4faMqI1bVCvzacXMW0="

c = Console(host=console_ip, port=console_port, key=console_key)

print(Dashboard(console=c).show())
```

Dashboard overview

```bash
Dashboard for dnsdist

Global:
        Uptime (seconds): 11887
        Number of queries: 68
        Query per second: 0
        ACL drops: 0
        Dynamic drops: 0
        Rule drops: 0
        CPU Usage (%s): 3.4
        Cache hitrate: 0
Servers:
        #0 / -- / dns_other
                Number of queries: 0
                Query per second: 0
                Number of drops: 0
        #1 / -- / dns_internal
                Number of queries: 1
                Query per second: 0
                Number of drops: 0
        #2 / -- / dns_internet
                Number of queries: 2
                Query per second: 68
                Number of drops: 2
        #3 / dns / --
                Number of queries: 3
                Query per second: 0
                Number of drops: 0

Ctrl+C to exit
```