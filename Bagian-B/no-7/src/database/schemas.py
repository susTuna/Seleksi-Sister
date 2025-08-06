from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    name: str
    email: str

class ClientCreate(ClientBase):
    client_id: str
    secret: str
    uri: Optional[str] = None

class Client(ClientBase):
    client_id: str
    uri: Optional[str] = None
    secret: str
    created_at: datetime
    is_active: bool = True

    class Config:
        orm_mode = True

class ClientRegister(ClientBase):
    uri: Optional[str] = None

    class Config:
        from_attributes = True

class AccessTokenBase(BaseModel):
    client_id: str
    token: str

class AccessTokenCreate(AccessTokenBase):
    issued_at: datetime
    expires_at: datetime

class AccessToken(AccessTokenBase):
    token_id: int
    issued_at: datetime
    expires_at: datetime
    is_revoked: bool = False

    class Config:
        orm_mode = True

class CustomWordListBase(BaseModel):
    client_id: str
    whitelist: str
    blacklist: str

class CustomWordListCreate(CustomWordListBase):
    pass

class CustomWordList(CustomWordListBase):
    list_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class WordListBase(BaseModel):
    name: str
    description: Optional[str] = None

class WordListCreate(WordListBase):
    pass

class WordList(WordListBase):
    list_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UsageLogBase(BaseModel):
    client_id: str
    endpoint: str
    timestamp: datetime
    size: int
    is_successful: bool = True
    error_message: Optional[str] = None

class UsageLogCreate(UsageLogBase):
    timestamp: datetime

class UsageLog(UsageLogBase):
    log_id: int
    timestamp: datetime

    class Config:
        orm_mode = True