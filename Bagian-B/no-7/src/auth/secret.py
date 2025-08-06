import base64
from random import randint
from hashlib import blake2b, shake_256, sha3_224, md5, sha1, sha384
from dotenv import load_dotenv
from typing import Optional
from database.schemas import ClientRegister
import os

load_dotenv()

KEY = os.getenv("BKEY").encode()
SALT = os.getenv("BSALT").encode()
PERSON = os.getenv("BPERSON").encode()

def concat_secret(name: str, email: str, uri: Optional[str] = None) -> str:
    if uri:
        return f"{name[:1]}:{email[2:]}:{uri[:5]}:{email[:2]}:{name[1:]}"
    return f"{name[:1]}:{email[2:]}:{email[:2]}:{name[1:]}"

def fun_roulette() -> int:
    return randint(1,6)

def generate_password_p1(client: ClientRegister) -> str:
    secret = base64.b85encode(concat_secret(client.name, client.email, client.uri).encode()).decode()
    match fun_roulette():
        case 1:
            return sha384(secret.encode()).hexdigest()
        case 2:
            return blake2b(secret.encode(), digest_size=32, key=KEY, salt=SALT, person=PERSON).hexdigest()
        case 3:
            return shake_256(secret.encode()).hexdigest(32)
        case 4:
            return sha3_224(secret.encode()).hexdigest()
        case 5:
            return md5(secret.encode()).hexdigest()
        case 6:
            return sha1(secret.encode()).hexdigest()

def generate_password(client: ClientRegister) -> str:
    return base64.b64encode(generate_password_p1(client).encode()).decode()
