from database.database import SessionLocal
from database.crud import get_custom_word_list, create_custom_word_list, update_custom_word_list
from database.schemas import CustomWordListCreate
from api.token.token import get_current_client
from auth.oauth import oauth
from fastapi import APIRouter, HTTPException, status, Header, Depends
from pydantic import BaseModel

router = APIRouter()

class CWordRequest(BaseModel):
    action : str
    category : str
    words : str

@router.post('/custom-words')
async def update_cword(request: CWordRequest, authorization: str = Header(None), client: str = Depends(get_current_client)):
    oauth(authorization)
    db = SessionLocal()
    try:
        if not request.action or not request.category or not request.words:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: action, category, words"
            )
        elif request.action not in ['add', 'remove']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid action. Use 'add' or 'remove'."
            )
        elif request.category not in ['whitelist', 'blacklist']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category. Use 'whitelist' or 'blacklist'."
            )
        elif not request.words.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Words field cannot be empty"
            )
        new_words_list = [word.strip() for word in request.words.split(',') if word.strip()]
        if not new_words_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid words provided"
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
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cannot delete words from an empty list"
                )
            elif request.category == 'whitelist':
                updated_words = existing_whitelist.difference(new_words_list)
                custom_words_list['whitelist'] = ', '.join(updated_words)
            else:
                updated_words = existing_blacklist.difference(new_words_list)
                custom_words_list['blacklist'] = ', '.join(updated_words)
        update_custom_word_list(db, client.client_id, custom_words_list)
        return { "message" : "Success"}
    finally:
        db.close()