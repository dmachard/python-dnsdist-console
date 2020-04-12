# Python client for dnsdist console

![](https://github.com/dmachard/dnsdist_console/workflows/Publish%20to%20PyPI/badge.svg)

| | |
| ------------- | ------------- |
| Author |  Denis Machard <d.machard@gmail.com> |
| License |  MIT | 
| PyPI |  https://pypi.org/project/dnsdist_console/ |
| | |

This is a Python client for the dnsdist console

## Table of contents
* [Installation](#installation)
* [Authentication](#authentication)
* [Send command to the console](#send-command-to-the-console)
* [Generate key](#generate-key)

## Installation

```python
pip install dnsdist_console
```

## Authentication

```python
from dnsdist_console import Console
```
 
## Send command to the console

```python
from dnsdist_console import Console

console_ip = "127.0.0.1"
console_port = 5199
console_key = "GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag="

console = Console(host=console_ip,
                  port=console_port, 
                  key=console_key)
            
o = console.send_command(cmd="showVersion()")
print(o)
```

## Generate key

```python
from dnsdist_console import Key

k = Key().generate()
print(k)
```