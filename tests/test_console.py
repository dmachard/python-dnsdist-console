
from dnsdist_console import Console

# dnsdist console
console_ip = "127.0.0.1"
console_port = 5199
console_key = "GQpEpQoIuzA6kzgwDokX9JcXPXFvO1Emg1wAXToJ0ag="

console = Console(host=console_ip,
                  port=console_port, 
                  key=console_key)
            
o = console.send_command(cmd="showVersion()")
print(o)

o = console.send_command(cmd="showServers()")
print(o)
