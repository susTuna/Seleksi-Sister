from http.client import HTTPResponse, HTTPConnection
import requests
import json, os
from dotenv import load_dotenv
from src.totp.totpgen import generate_totp

load_dotenv()

URL = os.getenv("BACKEND_URL")

def get_math():
    try:
        conn = HTTPConnection(URL)
        conn.request("GET", "/challenge-math")
        response: HTTPResponse = conn.getresponse()
        if response.status != 200:
            return None
        data: bytes = response.read()
        return json.loads(data.decode('utf-8')).get("question")
    except Exception as e:
        print(f"Error fetching math challenge: {e}")
        return None
    
def activate_account(payload):
    try:
        response = requests.post(
            f"http://{URL}/activate-account", 
            json=payload
        )
        if response.status_code != 200:
            print(f"Server returned error: Status {response.status_code}")
            print(f"Error details: {json.dumps(response.json(), indent=4)}")
        else:
            formatted_json = json.dumps(response.json(), indent=4)
            print(f"Account activation successful:\n{formatted_json}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error activating account: {e}")
    
def stage_a_submit(payload, file):
    try:
        response = requests.post(
            f"http://{URL}/stage-a/submit", 
            data=payload,
            files=file
        )

        if response.status_code != 200:
            print(f"Server returned error: Status {response.status_code}")
            print(f"Error details: {json.dumps(response.json(), indent=4)}")
        else:
            formatted_json = json.dumps(response.json(), indent=4)
            print(f"Submission successful:\n{formatted_json}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting stage A: {e}")

def update_public_key(payload):
    try:
        conn = HTTPConnection(URL)
        headers = {
            'Content-Type': 'application/json',
        }
        conn.request("POST", "/update-public-key", json.dumps(payload), headers)
        response: HTTPResponse = conn.getresponse()
        data: bytes = response.read()
        
        if response.status_code != 200:
            print(f"Server returned error: Status {response.status_code}")
            print(f"Error details: {json.dumps(response.json(), indent=4)}")
        else:
            formatted_json = json.dumps(response.json(), indent=4)
            print(f"Public key updated successfully:\n{formatted_json}")
        return response.json()
    except Exception as e:
        print(f"Error updating public key: {e}")
        return None
    
def get_submissions(user, payload):
    try:
        response = requests.get(
            f"http://{URL}/user/{user}/submissions?totp_code={payload}", 
        )
        if response.status_code != 200:
            print(f"Server returned error: Status {response.status_code}")
            print(f"Error details: {json.dumps(response.json(), indent=4)}")
        else:
            formatted_json = json.dumps(response.json(), indent=4)
            print(f"Submissions fetched successfully:\n{formatted_json}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching submissions: {e}")