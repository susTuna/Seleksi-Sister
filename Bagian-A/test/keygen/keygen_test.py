from src.keygen.keygen import Keygen
from pqcrypto.sign import sphincs_shake_256s_simple
import base64


K = Keygen(sphincs_shake_256s_simple)

K.generate_keypair()
print(f"public: {base64.b64encode(K.get_public_key())}")
print(f"private: {base64.b64encode(K.get_private_key())}")

