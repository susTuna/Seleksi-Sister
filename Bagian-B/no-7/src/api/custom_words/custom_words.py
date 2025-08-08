from database.database import SessionLocal
from database.crud import get_custom_word_list, create_custom_word_list, update_custom_word_list
from database.schemas import CustomWordListCreate
from utils.ratelimit import rate_limiter
from auth.oauth import oauth
from utils.logger import log_usage
from fastapi import APIRouter, HTTPException, status, Header, Depends
from pydantic import BaseModel

router = APIRouter()

class CWordRequest(BaseModel):
    action : str
    category : str
    words : str

@router.post('/custom-words')
async def update_cword(request: CWordRequest, authorization: str = Header(None), client: str = Depends(rate_limiter)):
    oauth(authorization)
    db = SessionLocal()
    try:
        size = len(request.json().encode())
        if not request.action or not request.category or not request.words:
            error_msg = "Missing required fields: action, category, words"
            log_usage(client.client_id, "/custom-words", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        elif request.action not in ['add', 'remove']:
            error_msg = "Invalid action. Use 'add' or 'remove'."
            log_usage(client.client_id, "/custom-words", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        elif request.category not in ['whitelist', 'blacklist']:
            error_msg= "Invalid category. Use 'whitelist' or 'blacklist'."
            log_usage(client.client_id, "/custom-words", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        elif not request.words.strip():
            error_msg = "Words field cannot be empty"
            log_usage(client.client_id, "/custom-words", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        new_words_list = [word.strip() for word in request.words.split(',') if word.strip()]
        if not new_words_list:
            error_msg = "No valid words provided"
            log_usage(client.client_id, "/custom-words", size, False, error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        custom_words_list = get_custom_word_list(db, client.client_id)
        if not custom_words_list:
            custom_words_list = CustomWordListCreate({
                'client_id': client.client_id,
                'whitelist': '',
                'blacklist': ''
            })
            create_custom_word_list(db, custom_words_list)
        existing_whitelist = set(custom_words_list.whitelist.split(', ')) if custom_words_list.whitelist else set()
        existing_blacklist = set(custom_words_list.blacklist.split(', ')) if custom_words_list.blacklist else set()
        if request.action == 'add':
            if request.category == 'whitelist':
                updated_words = existing_whitelist.union(new_words_list)
                custom_words_list['whitelist'] = ', '.join(updated_words)
            else:
                updated_words = existing_blacklist.union(new_words_list)
                custom_words_list['blacklist'] = ', '.join(updated_words)
        else:  # request.action == 'remove'
            if existing_blacklist == set() or existing_whitelist == set():
                error_msg = "Cannot remove words from an empty list"
                log_usage(client.client_id, "/custom-words", size, False, error_msg)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=error_msg
                )
            elif request.category == 'whitelist':
                updated_words = existing_whitelist.difference(new_words_list)
                custom_words_list['whitelist'] = ', '.join(updated_words)
            else:
                updated_words = existing_blacklist.difference(new_words_list)
                custom_words_list['blacklist'] = ', '.join(updated_words)
        update_custom_word_list(db, client.client_id, custom_words_list)
        log_usage(client.client_id, "/custom-words", size, True)
        return { "message" : "Success"}
    finally:
        db.close()