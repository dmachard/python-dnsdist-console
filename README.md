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

```python
from dnsdist_console import Statistics

print(Statistics(console=console))
{'global': {'acl-drops': '0', 'latency0-1': '0', 'cache-hits': '0', 'latency1-10': '0', 'cache-misses': '0', 'latency10-50': '0', 'cpu-sys-msec': '60748', 'latency100-1000': '0', 'cpu-user-msec': '85918', 'latency50-100': '0', 'downstream-send-errors': '0', 'no-policy': '0', 'downstream-timeouts': '0', 'noncompliant-queries': '0', 'dyn-block-nmg-size': '0', 'noncompliant-responses': '0', 'dyn-blocked': '0', 'queries': '0', 'empty-queries': '0', 'rdqueries': '0', 'fd-usage': '26', 'real-memory-usage': '1224421376', 'frontend-noerror': '0', 'responses': '0', 'frontend-nxdomain': '0', 'rule-drop': '0', 'frontend-servfail': '0', 'rule-nxdomain': '0', 'latency-avg100': '0.0', 'rule-refused': '0', 'latency-avg1000': '0.0', 'rule-servfail': '0', 'latency-avg10000': '0.0', 'security-status': '0', 'latency-avg1000000': '0.0', 'self-answered': '0', 'latency-count': '0', 'servfail-responses': '0', 'latency-slow': '0', 'special-memory-usage': '83423232', 'latency-sum': '0', 'trunc-failures': '0', 'uptime': '67846'}, 'backends': [{'#': '0', 'name': '', 'address': '10.0.0.140:53', 'state': 'UP', 'qps': '0.0', 'qlim': '0', 'ord': '1', 'wt': '1', 'queries': '0', 'drops': '0', 'drate': '0.0', 'lat': '0.0', 'outstanding': '0', 'pools': 'dns_others'}, {'#': '1', 'name': '', 'address': '10.0.0.55:53', 'state': 'UP', 'qps': '0.0', 'qlim': '0', 'ord': '1', 'wt': '1', 'queries': '0', 'drops': '0', 'drate': '0.0', 'lat': '0.0', 'outstanding': '0', 'pools': 'dns_internal'}, {'#': '2', 'name': '', 'address': '8.8.8.8:53', 'state': 'UP', 'qps': '0.0', 'qlim': '0', 'ord': '1', 'wt': '1', 'queries': '0', 'drops': '0', 'drate': '0.0', 'lat': '0.0', 'outstanding': '0', 'pools': 'dns_internet'}, {'#': '3', 'name': 'dns1', 'address': '1.1.1.1:53', 'state': 'up', 'qps': '0.0', 'qlim': '0', 'ord': '1', 'wt': '1', 'queries': '0', 'drops': '0', 'drate': '0.0', 'lat': '0.0', 'outstanding': '0', 'pools': ''}]}
```

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