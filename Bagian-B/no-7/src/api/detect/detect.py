from database.database import SessionLocal
from database.crud import get_word_list, get_custom_word_list
from api.token.token import get_current_client
from algorithm.process import VeritasShield
from auth.oauth import oauth
from utils.logger import log_usage
from fastapi import APIRouter, HTTPException, status, Header, Depends
from pydantic import BaseModel

router = APIRouter()

class DetectRequest(BaseModel):
    text: str

WORD_LIST = get_word_list(SessionLocal())

@router.post("/detect")
async def detect_text(request: DetectRequest, authorization: str = Header(None), client: str = Depends(get_current_client)):
    oauth(authorization)
    db = SessionLocal()
    try:
        size = len(request.json().encode())
        if not request.text:
            error_msg = "Text field is required"
            log_usage(client.client_id, "/detect", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        custom_word_list = get_custom_word_list(db, client.client_id)
        word_list = (WORD_LIST.description.split(', '))
        if custom_word_list:
            whitelist = set(custom_word_list.whitelist.split(', '))
            blacklist = set(custom_word_list.blacklist.split(', '))
            word_list = list(set(word_list) - whitelist | blacklist)
        text = request.text

        shield = VeritasShield(1024)
        detected_words = shield.find_patterns(word_list, text)

        log_usage(
            client.client_id,
            "/detect",
            size,
            True
        )

        if not detected_words:
            return {"isProfane" : False, "message": "No sensitive words detected"}
        
        return {"isProfane" : True, "detected_words": detected_words}

    finally:
        db.close()