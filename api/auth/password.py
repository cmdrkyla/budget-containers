import codecs
import hashlib
from random import SystemRandom

from config import STRING_ENCODING


HASH_ALGORITHM = "pbkdf2"
HASH_FUNCTION = "sha256"
HASH_ITERATIONS = 150000
SALT_LENGTH = 10
SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SYSTEM_RNG = SystemRandom()


class Password:
    @classmethod
    def hash_password(self, password: str, salt_length: int=0):
        salt = self.generate_salt(salt_length)
        hash = self._hash_password(password, salt)
        method = self._hash_method()
        return "$".join([method, salt, hash])
    
    
    @classmethod
    def check_password(self, provided_password: str, full_hash: str):
        _, _, _, salt, valid_hash = full_hash.split("$", 4)
        unknown_hash = self._hash_password(provided_password, salt)
        if unknown_hash == valid_hash:
            return True
        else:
            return False

    @classmethod
    def generate_salt(self, length: int=0):
        if length < SALT_LENGTH:
            length = SALT_LENGTH
        return "".join(SYSTEM_RNG.choice(SALT_CHARS) for _ in range(length))
    

    def _hash_password(password: str, salt: str):
        hash_bytes = hashlib.pbkdf2_hmac(
            hash_name = HASH_FUNCTION,
            password = bytes(password.encode(STRING_ENCODING)), 
            salt = bytes(salt.encode(STRING_ENCODING)), 
            iterations = HASH_ITERATIONS,
        )
        
        return codecs.encode(hash_bytes, "hex_codec").decode(STRING_ENCODING)


    def _hash_method():
        return f"{HASH_ALGORITHM}${HASH_FUNCTION}${HASH_ITERATIONS}"