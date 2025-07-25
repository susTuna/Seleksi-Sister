from hashlib import sha256
from random import randint

class Nonce:
    def __init__ (self, pow_prefix, diff):
        self.nonce = 0 # starts at 0
        self.pow_prefix = pow_prefix
        self.test_str = f"{self.pow_prefix}:{self.nonce}"
        self.algorithm = sha256
        self.target = "0" * diff
    
    def generate_nonce(self):
        self.nonce = randint(0, 2**32 - 1)

    def set_test_str(self):
        self.test_str = f"{self.pow_prefix}:{self.nonce}" #update test_str with new nonce
    
    def get_nonce(self):
        return self.nonce

    def create_hash(self):
        self.hash = self.algorithm(self.test_str.encode()).hexdigest()
    
    def get_hash(self):
        return self.hash
    
    def is_valid(self):
        return self.hash.startswith(self.target)