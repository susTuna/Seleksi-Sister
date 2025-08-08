from fastapi import HTTPException, status, Header
from database.database import SessionLocal
from database.crud import revoke_token_by_date
from datetime import datetime
from zoneinfo import ZoneInfo

def oauth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
def revoke():
    db = SessionLocal()
    try:
        current_date = datetime.now(ZoneInfo('Asia/Jakarta'))
        revoked_tokens = revoke_token_by_date(db, current_date)
        if not revoked_tokens:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No tokens found to revoke"
            )
        return {"message": "Tokens revoked successfully", "revoked_tokens": len(revoked_tokens)}
    finally:
        db.close()