from src.api.routes import get_submissions
from src.totp.totpgen import generate_totp
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
payload = {
    "totp_code": generate_totp(),
}
get_submissions(USERNAME, generate_totp())
