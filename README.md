# Python client for dnsdist console

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dnsdist-console)
![](https://github.com/dmachard/dnsdist_console/workflows/Publish%20to%20PyPI/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

| | |
| ------------- | ------------- |
| Author |  Denis Machard <d.machard@gmail.com> 
| License |  MIT | 
| PyPI |  https://pypi.org/project/dnsdist_console/ |
| | |

This is a Python 3 client for the dnsdist console. You can use it to execute remote commands, 
display a dashboard or easily extract statistics.


## Table of contents
* [Installation](#installation)
* [Generate key](#generate-key)
* [Handshake](#handshake)
* [Run command](#run-command)
* [Get statistics](#get-statistics)
* [Display dashboard](#display-dashboard)

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

## Handshake

Configure the client with the IP address and the TCP port of your dnsdist as well as the associated secret key.
If the provided key is incorrect, an exception will be raised.

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

Please refer to the [dnsdist documentation](https://dnsdist.org/reference/config.html) for available commands.

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

print(Statistics(console=console))
```

List of availables keys and descriptions:

- globals (dict):
    - acl-drops
    - latency0-1
    - cache-hits
    - latency1-10
    - cache-misses
    - latency10-50
    - cpu-sys-msec
    - latency100-1000
    - cpu-user-msec
    - latency50-100
    - downstream-send-errors
    - no-policy
    - downstream-timeouts
    - noncompliant-queries
    - dyn-block-nmg-size
    - noncompliant-responses
    - dyn-blocked
    - queries
    - empty-queries
    - rdqueries
    - fd-usage
    - real-memory-usage
    - frontend-noerror
    - responses
    - frontend-nxdomain
    - rule-drop
    - frontend-servfail
    - rule-nxdomain
    - latency-avg100
    - rule-refused
    - latency-avg1000
    - rule-servfail
    - latency-avg10000
    - security-status
    - latency-avg1000000
    - self-answered
    - latency-count
    - servfail-responses
    - latency-slow
    - special-memory-usage
    - latency-sum
    - trunc-failures
    - uptime

- backends (list):
    - #
    - name
    - address
    - state
    - qps
    - qlim
    - ord
    - wt
    - queries
    - drops
    - drate
    - lat
    - outstanding
    - pools

## Display dashboard

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