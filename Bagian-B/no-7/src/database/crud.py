from sqlalchemy.orm import Session
from database import database, models, schemas
from datetime import datetime

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(
        name=client.name,
        email=client.email,
        secret=client.secret,
        uri=client.uri,
        created_at=datetime.now('Asia/Jakarta')
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def create_token(db: Session, token: schemas.AccessTokenCreate):
    db_token = models.AccessToken(
        client_id=token.client_id,
        token=token.token,
        issued_at=token.issued_at,
        expires_at=token.expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def create_custom_word_list(db: Session, word_list: schemas.CustomWordListCreate):
    db_word_list = models.CustomWordList(
        client_id=word_list.client_id,
        whitelist=word_list.whitelist,
        blacklist=word_list.blacklist,
        created_at=datetime.now('Asia/Jakarta'),
        updated_at=datetime.now('Asia/Jakarta')
    )
    db.add(db_word_list)
    db.commit()
    db.refresh(db_word_list)
    return db_word_list

def create_word_list(db: Session, word_list: schemas.WordListCreate):
    db_word_list = models.WordList(
        name=word_list.name,
        description=word_list.description,
        created_at=datetime.now('Asia/Jakarta'),
        updated_at=datetime.now('Asia/Jakarta')
    )
    db.add(db_word_list)
    db.commit()
    db.refresh(db_word_list)
    return db_word_list

def create_usage_log(db: Session, log: schemas.UsageLogCreate):
    db_log = models.UsageLog(
        client_id=log.client_id,
        endpoint=log.endpoint,
        timestamp=log.timestamp,
        size=log.size,
        is_successful=log.is_successful,
        error_message=log.error_message
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def update_custom_word_list(db: Session, user_id: int, word_list: schemas.CustomWordListCreate):
    db_word_list = db.query(models.CustomWordList).filter(models.CustomWordList.user_id == user_id).first()
    if db_word_list:
        db_word_list.whitelist = word_list.whitelist
        db_word_list.blacklist = word_list.blacklist
        db_word_list.updated_at = datetime.now('Asia/Jakarta')
        db.commit()
        db.refresh(db_word_list)
    return db_word_list

def update_word_list(db: Session, list_id: int, word_list: schemas.WordListCreate):
    db_word_list = db.query(models.WordList).filter(models.WordList.list_id == list_id).first()
    if db_word_list:
        db_word_list.name = word_list.name
        db_word_list.description = word_list.description
        db_word_list.updated_at = datetime.now('Asia/Jakarta')
        db.commit()
        db.refresh(db_word_list)
    return db_word_list

def revoke_token(db: Session, token_id: int):
    db_token = db.query(models.AccessToken).filter(models.AccessToken.token_id == token_id).first()
    if db_token:
        db_token.is_revoked = True
        db.commit()
        db.refresh(db_token)
    return db_token

def revoke_token_by_date(db: Session, date: datetime):
    db_tokens = db.query(models.AccessToken).filter(
        models.AccessToken.expires_at < date
    ).all()
    for token in db_tokens:
        token.is_revoked = True
    db.commit()
    return db_tokens

def get_client(db: Session, name: str):
    return db.query(models.Client).filter(models.Client.name == name).first()

def get_token(db: Session, client_id: int):
    return db.query(models.AccessToken.token).filter(
        models.AccessToken.client_id == client_id,
        models.AccessToken.is_revoked == False
        ).first()

def get_word_list(db: Session):
    return db.query(models.WordList.description).all()

def get_custom_word_list(db: Session, client_id: int):
    return db.query(models.CustomWordList.blacklist, models.CustomWordList.whitelist).filter(
        models.CustomWordList.client_id == client_id
    ).first()