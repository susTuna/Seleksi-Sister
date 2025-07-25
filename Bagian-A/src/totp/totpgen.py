import base64
from dotenv import load_dotenv
import os
import pyotp
import time

load_dotenv()

SECRET = os.getenv("TOTP_SECRET")

def generate_totp():
    totp = pyotp.TOTP(base64.b32encode(SECRET.encode('utf-8')))
    current_totp = totp.now()
    return current_totp