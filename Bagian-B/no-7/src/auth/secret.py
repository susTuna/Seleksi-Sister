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

def generate_id_key(msg: str, key: str) -> str:
    key = list(key)
    if len(msg) == len(key): return key
    for i in range(len(msg) - len(key)):
        key.append(key[i % len(key)])
    return ''.join(key)

def generate_id_p1(msg: str, key: str) -> str:
    id = []
    key = generate_id_key(msg, key)
    for i in range(len(msg)):
        char = msg[i]
        if char.isupper():
            id.append(chr((ord(char) + ord(key[i]) - 2 * ord('A')) % 26 + ord('A')))
        elif char.islower():
            id.append(chr((ord(char) + ord(key[i]) - 2 * ord('a')) % 26 + ord('a')))
        elif char.isdigit():
            id.append(chr((ord(char) + ord(key[i]) - 2 * ord('0')) % 10 + ord('0')))
        else:
            id.append(char)
    return ''.join(id)

def generate_id(client: ClientRegister) -> str:
    msg = concat_secret(client.name, client.email, client.uri)
    key = base64.b64encode(msg[:9].encode()).decode()
    return generate_id_p1(msg, key)

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
