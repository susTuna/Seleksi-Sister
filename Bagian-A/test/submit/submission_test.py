from src.api.routes import stage_a_submit
from src.mathsolver.solver import MathSolver
from src.totp.totpgen import generate_totp
from src.keygen.keygen import Keygen
from pqcrypto.sign import sphincs_shake_256s_simple
import os
import hashlib
import argparse
import base64
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit your solution")
    parser.add_argument("--file", "-f", type=str, required=True, help="Path to the file containing the solution")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File {args.file} does not exist.")
        exit(1)

    M = MathSolver()

    K = Keygen(sphincs_shake_256s_simple)

    # Load keys from environment variables
    public_key = os.getenv("PUBLIC_KEY")
    private_key = os.getenv("PRIVATE_KEY")
    K.set_private_key(base64.b64decode(private_key))
    K.set_public_key(base64.b64decode(public_key))
    print(public_key)

    # Load username
    username = os.getenv("USERNAME")

    try:
        with open(args.file, "rb") as file:
            file_content = file.read()
            if not file_content:
                print("File is empty.")
                exit(1)
            # Sign the file
            K.sign(file_content)
            signature = K.get_signature()
            b64signature = base64.b64encode(signature).decode()
        files = {
        "file": (os.path.basename(args.file), file_content, 'application/pdf')
        }
    except FileNotFoundError:
        print(f"File {args.file} not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading file {args.file}: {e}")
        exit(1)
    
    if files is None:
        print("File content is empty.")
        exit(1)

    # Generate TOTP
    totp = generate_totp()
    # Get math challenge
    challenge = M.get_challenge()
    M.solve()
    result = M.get_result()

    # verify the signature
    if not K.is_valid(file_content, signature):
        print("Signature verification failed.")
        exit(1)

    # Prepare payload
    payload = {
        "username" : username,
        "totp_code" : totp,
        "math_question" : challenge,
        "math_answer" : result,
        "signature" : b64signature,
        "tahap" : 1
    }

    # Submit the payload
    response = stage_a_submit(payload, files)
    if response.get("status") == "success":
        print("Submission successful!")
        print(f"Message: {response.get('message')}")
    else:
        print("Submission failed.")
        print(f"Message: {response.get('message')}")
        exit(1)




