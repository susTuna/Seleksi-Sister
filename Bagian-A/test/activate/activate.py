from dotenv import load_dotenv
from src.api.routes import activate_account
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
N = os.getenv("NONCE")
PUB = os.getenv("PUBLIC_KEY")

payload = {
    "username": USERNAME,
    "password": PASSWORD,
    "nonce": N,
    "public_key": PUB
}

response = activate_account(payload)
if response:
    print("Account activation response:", response)
else:
    print("Failed to activate account.")