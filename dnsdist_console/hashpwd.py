import base64
import secrets
import scrypt

class HashPassword:
    def generate(self, password, work_factor=10, parallel_factor=1, block_size=8, salt_size=16, output_size=32, pwhash_prefix="$scrypt$"):
        """generate hash password for web server"""
        result = []
        result.append(pwhash_prefix)

        result.append("ln=")
        result.append("%s" % work_factor)

        result.append(",p=")
        result.append("%s" % parallel_factor)

        result.append(",r=")
        result.append("%s" % block_size)

        result.append("$")
        salt = secrets.token_bytes(salt_size)
        result.append("%s" % base64.b64encode(salt).decode())
        result.append("$")

        out = scrypt.hash(password, salt, N=2**work_factor, p=parallel_factor, r=block_size, buflen=output_size)
        result.append("%s" % base64.b64encode(out).decode())

        return "".join(result)