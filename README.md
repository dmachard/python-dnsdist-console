# Python client for dnsdist console

![](https://github.com/dmachard/dnsdist_console/workflows/Publish%20to%20PyPI/badge.svg)

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

Save-it in your `/etc/dnsdist/dnsdist.conf` with the `setKey` directive.

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
