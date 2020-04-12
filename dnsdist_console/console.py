
import socket
import libnacl
import libnacl.utils
import struct
import base64

class Console:
    def __init__(self, key,
		       host="127.0.0.1",
                       port=5199):
        """authenticator class"""
        self.console_host = host
        self.console_port = port
        self.console_key = base64.b64decode(key) 
        
        self.nonce_c = libnacl.utils.rand_nonce()
        self.nonce_s = None
        
        self.sock = None
        self.sock_timeout = 1.0
        
        self.connect_to()

    def encrypt_command(self, cmd, nonce):
        """encrypt console"""
        cmd = cmd.encode('utf-8')
        return libnacl.crypto_secretbox(cmd, nonce, self.console_key)
        
    def decrypt_response(self, cmd, nonce):
        """decrypt console"""
        result = libnacl.crypto_secretbox_open(cmd, nonce, self.console_key)
        return result.decode('utf-8')
        
    def connect_to(self):
        """connect to console"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.settimeout(self.sock_timeout)

        self.sock.connect((self.console_host, self.console_port))
        self.sock.send(self.nonce_c)
        
        self.nonce_s = self.sock.recv(len(self.nonce_c))
        if len(self.nonce_s) != len(self.nonce_c):
            raise Exception("incorrect nonce size")
  
    def send_command(self, cmd):
        """send command to console and return output"""
        half_nonce = int(len(self.nonce_c) / 2)
        reading_nonce = self.nonce_c[0:half_nonce] + self.nonce_s[half_nonce:]
        writing_nonce = self.nonce_s[0:half_nonce] + self.nonce_c[half_nonce:]
        
        encrypted_cmd = self.encrypt_command(cmd, writing_nonce)
        
        self.sock.send(struct.pack("!I", len(encrypted_cmd)))
        self.sock.send(encrypted_cmd)
        
        data = self.sock.recv(4)
        if not data:
            raise Exception("no response size received")
            
        (response_size,) = struct.unpack("!I", data)
        data = self.sock.recv(response_size)
        return self.decrypt_response(data, reading_nonce)
