from database.database import SessionLocal
from database.schemas import AccessTokenCreate
from database.crud import create_token, get_client, get_token
from auth.oauth import oauth
from fastapi import APIRouter, HTTPException, status, Header, Depends
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
async def issue_token(request: TokenRequest, authorization: str = Header(None)):
    print(f"Received request: {request}, Authorization: {authorization}")
    if request.grant_type != "client_credentials":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant type"
        )
    oauth(authorization)
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
        
async def get_current_client(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        access_token = get_token(db, token)
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        elif access_token.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revoked",
                headers={"WWW-Authenticate": "Bearer"}
            )
        elif access_token.expires_at < datetime.now(ZoneInfo('Asia/Jakarta')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
        client = get_client(db, access_token.client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return client
    finally:
        db.close()