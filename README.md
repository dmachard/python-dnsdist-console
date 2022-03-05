# Python client for dnsdist console

Tool to interact with your dnsdist console from Python.

![powerdns dnsdist 1.6.x](https://img.shields.io/badge/dnsdist%201.6.x-tested-green) ![powerdns dnsdist 1.7.x](https://img.shields.io/badge/dnsdist%201.7.x-tested-green) ![python 3.8.x](https://img.shields.io/badge/python%203.8.x-tested-blue) ![python 3.9.x](https://img.shields.io/badge/python%203.9.x-tested-blue) ![python 3.10.x](https://img.shields.io/badge/python%203.10.x-tested-blue) 

## Table of contents
* [Installation](#installation)
* [Generate console key](#generate-console-key)
* [Generate hash password](#generate-hash-password)
* [Run command](#run-command)
* [Get statistics](#get-statistics)
* [Display basic dashboard](#display-basic-dashboard)

## Installation

This module can be installed from [pypi](https://pypi.org/project/dnsdist_console/) website

```python
pip install dnsdist_console
```

## Generate console key

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

## Generate hash password

You can use this module to generate a hash for the webserver of your dnsdist.
Since 1.7.0 the password should be hashed and salted.

The command in one line 

```bash
python3 -c "from dnsdist_console import HashPassword as H;print(H().generate(\"bonjour\"))"
$scrypt$ln=10,p=1,r=8$SZmi+pjuZ4u7L4jhXIkLww==$VRW7BuYUjSVjkjDIK6J1VB/RWx2s4gbz+YXgflWspf8=
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