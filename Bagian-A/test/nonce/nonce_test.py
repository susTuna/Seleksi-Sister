from src.nonce.nonce import Nonce

N = Nonce("13523147:if:eldad", 5)
N.create_hash()
while not N.is_valid():
    N.generate_nonce()
    N.set_test_str()
    N.create_hash()
    print("Trying nonce:", N.get_nonce(), "Hash:", N.get_hash())
print(f"Nonce: {N.get_nonce()}")
