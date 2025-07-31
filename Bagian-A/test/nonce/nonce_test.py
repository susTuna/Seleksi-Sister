from src.nonce.nonce import Nonce
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
MAJOR = os.getenv("MAJOR")
PASSWORD = os.getenv("PASSWORD")

N = Nonce(f"{USERNAME}:{MAJOR}:{PASSWORD}", 5)
N.create_hash()
while not N.is_valid():
    N.generate_nonce()
    N.set_test_str()
    N.create_hash()
    print("Trying nonce:", N.get_nonce(), "Hash:", N.get_hash())
print(f"Nonce: {N.get_nonce()}")
