from database.database import SessionLocal
from database.schemas import AccessTokenCreate
from database.crud import create_token, get_client
from fastapi import APIRouter, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import bcrypt
import secrets
import base64
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token", auto_error=True)

class TokenRequest(BaseModel):
    grant_type: str

@router.post("/oauth/token")
async def get_token(request: TokenRequest, authorization: str = Header(None)):
    print(f"Received request: {request}, Authorization: {authorization}")
    if request.grant_type != "client_credentials":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant type"
        )
    if not authorization or not authorization.startswith("Basic "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Basic"}
        )
    try:
        credentials = base64.b64decode(authorization[6:]).decode()
        client_id, client_secret = credentials.split(":")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Basic"}
        )
    db = SessionLocal()
    try:
        client = get_client(db, client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client id",
                headers={"WWW-Authenticate": "Basic"}
            )
        if not bcrypt.checkpw(client_secret.encode(), client.secret.encode()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid secret",
                headers={"WWW-Authenticate": "Basic"}
            )
        token_value = secrets.token_urlsafe(32)
        expires_in = 90 * 24 * 60 * 60
        expiration_date = datetime.now(ZoneInfo('Asia/Jakarta')) + timedelta(seconds=expires_in)
        token = AccessTokenCreate(
            client_id=client.client_id,
            token=token_value,
            issued_at=datetime.now(ZoneInfo('Asia/Jakarta')),
            expires_at=expiration_date
        )
        create_token(db, token)
        return {
            "access_token": token_value,
            "token_type": "Bearer",
            "expires_in": expiration_date
        }
    finally:
        db.close()
        
