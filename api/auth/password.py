from passlib.hash import pbkdf2_sha256

HASH_ROUNDS = 50000
SALT_SIZE = 16

class Password:
    @classmethod
    def hash_password(self, password: str):
        hash_method = pbkdf2_sha256.using(rounds=HASH_ROUNDS, salt_size=SALT_SIZE)
        return hash_method.hash(password)
    
    
    @classmethod
    def verify_password(self, provided_password: str, password_hash: str):
        hash_method = pbkdf2_sha256.using(rounds=HASH_ROUNDS, salt_size=SALT_SIZE)
        return hash_method.verify(provided_password, password_hash)