class Keygen:
    def __init__ (self, instance):
        self.instance = instance
    
    def generate_keypair(self):
        self.public_key, self.private_key = self.instance.generate_keypair()
    
    def sign(self, message):
        self.is_generated()
        self.signature = self.instance.sign(self.private_key, message)
    
    def get_signature(self):
        self.is_generated()
        return self.signature
    
    def is_valid(self, message, signature):
        self.is_generated()
        return self.instance.verify(self.public_key, message, signature)
    
    def get_public_key(self):
        self.is_generated()
        return self.public_key
    
    def set_public_key(self, public_key):
        self.public_key = public_key

    def set_private_key(self, private_key):
        self.private_key = private_key

    def get_private_key(self):
        self.is_generated()
        return self.private_key

    def is_generated(self):
        if not hasattr(self, 'private_key'):
            raise ValueError("Private key not generated. Call generate_keypair() first.")

