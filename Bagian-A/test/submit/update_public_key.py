from src.api.routes import update_public_key
from src.mathsolver.solver import MathSolver
from src.totp.totpgen import generate_totp
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    M = MathSolver()

    # Load keys from environment variables
    public_key = os.getenv("PUBLIC_KEY")

    # Load username
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    # Generate TOTP
    totp = generate_totp()
    # Get math challenge
    challenge = M.get_challenge()
    M.solve()
    result = M.get_result()
    
    # Prepare payload
    payload = {
        "username" : username,
        "password" : password,
        "totp_code" : totp,
        "math_question" : challenge,
        "math_answer" : result,
        "new_public_key" : public_key,
    }

    # Submit the payload
    response = update_public_key(payload)
    if response.get("status") == "success":
        print("Update successful!")
        print(f"Message: {response.get('message')}")
    else:
        print("Update failed.")
        print(f"Message: {response.get('message')}")
        exit(1)




