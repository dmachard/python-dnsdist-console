
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
        self.nonce_w = None
        self.nonce_r = None

        self.sock = None
        self.sock_timeout = 1.0
        
        self.connect_to()

    def encrypt_command(self, cmd, nonce):
        """encrypt console"""
        cmd = cmd.encode('utf-8')
        return libnacl.crypto_secretbox(cmd, nonce, self.console_key)
        
    def decrypt_response(self, data, nonce):
        """decrypt console"""
        result = libnacl.crypto_secretbox_open(data, nonce, self.console_key)
        return result.decode('utf-8')
        
    def incremente_nonce(self, nonce):
        """incremente nonce"""
        v = int.from_bytes(nonce[:4], "big")
        v += 1
        return v.to_bytes(4, byteorder='big') + nonce[4:]

    def disconnect(self):
        """disconnect"""
        if self.sock is not None:
            self.sock.close()
        
    def connect_to(self):
        """connect to console"""
        # prepare socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.settimeout(self.sock_timeout)

        # connect to the server
        self.sock.connect((self.console_host, self.console_port))

        # send our nonce
        self.sock.send(self.nonce_c)
        
        # waiting to receive server nonce
        self.nonce_s = self.sock.recv(len(self.nonce_c))
        if len(self.nonce_s) != len(self.nonce_c):
            raise Exception("incorrect nonce size")
  
        # init reading and writing nonce
        half_nonce = int(len(self.nonce_c) / 2)
        self.nonce_r = self.nonce_c[0:half_nonce] + self.nonce_s[half_nonce:]
        self.nonce_w = self.nonce_s[0:half_nonce] + self.nonce_c[half_nonce:]

        # send empty command to check if the hanshake is ok
        try:
              self.send_command(cmd="")
        except Exception as e:
              raise Exception("hanshake error: %s" % e)

    def send_command(self, cmd):
        """send command to console and return output"""
        # encrypt command
        encrypted_cmd = self.encrypt_command(cmd, self.nonce_w)
        
        # send data size header
        self.sock.send(struct.pack("!I", len(encrypted_cmd)))

        # send encrypted command
        self.sock.send(encrypted_cmd)
        
        # waiting to receive data size
        data = self.sock.recv(4)
        if not data:
            raise Exception("no response size received")
            
        # unpack response size
        (response_size,) = struct.unpack("!I", data)

        # waiting to response response according to the response size
        data = self.sock.recv(response_size)
        while len(data) < response_size:
            data += self.sock.recv(response_size - len(data))

        # decrypt data
        r = self.decrypt_response(data, self.nonce_r)

        # incremente nonce for next command
        self.nonce_r = self.incremente_nonce(nonce=self.nonce_r)
        self.nonce_w = self.incremente_nonce(nonce=self.nonce_w)

        # return response output
        return r
