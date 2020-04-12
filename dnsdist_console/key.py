
import libnacl
import libnacl.utils
import base64

class Key:
    def generate(self):
        """generate console key"""
        k = libnacl.utils.salsa_key()
        return base64.b64encode(k).decode("utf8")
        
