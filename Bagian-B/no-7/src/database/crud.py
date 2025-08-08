from sqlalchemy.orm import Session
from database import database, models, schemas
from datetime import datetime
from zoneinfo import ZoneInfo

def create_client(db: Session, client: schemas.ClientCreate):
    try:
        db_client = models.Client(
            client_id=client.client_id,
            name=client.name,
            email=client.email,
            secret=client.secret,
            uri=client.uri,
            created_at=datetime.now(ZoneInfo('Asia/Jakarta'))
        )
        db.add(db_client)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_client)
        return db_client

def create_token(db: Session, token: schemas.AccessTokenCreate):
    try:
        db_token = models.AccessToken(
            client_id=token.client_id,
            token=token.token,
            issued_at=token.issued_at,
            expires_at=token.expires_at
        )
        db.add(db_token)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_token)
        return db_token

def create_custom_word_list(db: Session, word_list: schemas.CustomWordListCreate):
    try:
        db_word_list = models.CustomWordList(
            client_id=word_list.client_id,
            whitelist=word_list.whitelist,
            blacklist=word_list.blacklist,
            created_at=datetime.now(ZoneInfo('Asia/Jakarta')),
            updated_at=datetime.now(ZoneInfo('Asia/Jakarta'))
        )
        db.add(db_word_list)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_word_list)
        return db_word_list

def create_word_list(db: Session, word_list: schemas.WordListCreate):
    try:
        db_word_list = models.WordList(
            name=word_list.name,
            description=word_list.description,
            created_at=datetime.now(ZoneInfo('Asia/Jakarta')),
            updated_at=datetime.now(ZoneInfo('Asia/Jakarta'))
        )
        db.add(db_word_list)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_word_list)
        return db_word_list

def create_usage_log(db: Session, log: schemas.UsageLogCreate):
    try:
        db_log = models.UsageLog(
            client_id=log.client_id,
            endpoint=log.endpoint,
            timestamp=log.timestamp,
            size=log.size,
            is_successful=log.is_successful,
            error_message=log.error_message
        )
        db.add(db_log)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_log)
        return db_log

def update_custom_word_list(db: Session, user_id: int, word_list: schemas.CustomWordListCreate):
    try:
        db_word_list = db.query(models.CustomWordList).filter(models.CustomWordList.user_id == user_id).first()
        if db_word_list:
            db_word_list.whitelist = word_list.whitelist
            db_word_list.blacklist = word_list.blacklist
            db_word_list.updated_at = datetime.now(ZoneInfo('Asia/Jakarta'))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_word_list)
        return db_word_list

def update_word_list(db: Session, list_id: int, word_list: schemas.WordListCreate):
    try:
        db_word_list = db.query(models.WordList).filter(models.WordList.list_id == list_id).first()
        if db_word_list:
            db_word_list.name = word_list.name
            db_word_list.description = word_list.description
            db_word_list.updated_at = datetime.now(ZoneInfo('Asia/Jakarta'))
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_word_list)
        return db_word_list

def revoke_token(db: Session, token_id: int):
    try:
        db_token = db.query(models.AccessToken).filter(models.AccessToken.token_id == token_id).first()
        if db_token:
            db_token.is_revoked = True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        db.refresh(db_token)
        return db_token

def revoke_token_by_date(db: Session, date: datetime):
    try:
        db_tokens = db.query(models.AccessToken).filter(
            models.AccessToken.expires_at < date
        ).all()
        for token in db_tokens:
            token.is_revoked = True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
        return db_tokens

def get_client(db: Session, client_id: str):
    return db.query(models.Client).filter(models.Client.client_id == client_id).first()

def get_token(db: Session, token: str) -> models.AccessToken:
    access_token = db.query(models.AccessToken).filter(
        models.AccessToken.token == token
        ).first()
    if access_token and access_token.expires_at:
        if access_token.expires_at.tzinfo is None:
            access_token.expires_at = access_token.expires_at.replace(tzinfo=ZoneInfo('Asia/Jakarta'))
    return access_token

def get_word_list(db: Session):
    return db.query(models.WordList).first()

def get_custom_word_list(db: Session, client_id: str):
    return db.query(models.CustomWordList).filter(
        models.CustomWordList.client_id == client_id
    ).first()