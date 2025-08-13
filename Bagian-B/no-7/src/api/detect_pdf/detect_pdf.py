from database.database import SessionLocal
from utils.ratelimit import rate_limiter
from api.detect.detect import detect_text, DetectRequest
from auth.oauth import oauth
from utils.logger import log_usage
from fastapi import APIRouter, HTTPException, status, Header, Depends, File, UploadFile, Form
from dotenv import load_dotenv
import os, requests, time

router = APIRouter()

load_dotenv()

API_ID = os.getenv("API_ID")
API_SECRET = os.getenv("API_SECRET")
PDF_URL = os.getenv("PDF_URL")
TOKEN_PAYLOAD = {
            "grant_type": "client_credentials",
            "client_id": API_ID,
            "client_secret": API_SECRET
        }

token_cache = {}

def get_access_token():
    current_time = time.time()
    if token_cache and token_cache.get('expires_at', 0) > current_time:
        return token_cache['token']
    
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{PDF_URL}oauth/token",
        headers=headers,
        json=TOKEN_PAYLOAD
    )

    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get('access_token')

        token_cache['token'] = token
        token_cache['expires_at'] = current_time + (60 * 60)

        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to authenticate with PDF service"
        )
    
@router.post("/detect-pdf")
async def detect_pdf(file: UploadFile = File(...), authorization: str = Header(None), client: str = Depends(rate_limiter)):
    oauth(authorization)
    db = SessionLocal()
    try:
        file_content = await file.read()
        size = len(file_content)
        if file.content_type != "application/pdf":
            error_msg = "Only PDF files are accepted"
            log_usage(client.client_id, "/detect-pdf", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        files = {
            'file': (file.filename, file_content, 'application/pdf')
        }

        pdf_response = requests.post(
            f"{PDF_URL}extract-text/",
            headers=headers,
            files=files
        )

        if pdf_response.status_code != 200:
            error_msg = f"PDF service error : {pdf_response}"
            log_usage(client.client_id, "/detect-pdf", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to process PDF file"
            )
        
        pdf_data = pdf_response.json()
        text = DetectRequest(text=pdf_data.get('text', ''))

        detect_response = await detect_text(text, authorization, client)
        return detect_response
    finally:
        db.close()