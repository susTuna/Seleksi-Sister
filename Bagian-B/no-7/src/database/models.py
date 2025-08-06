from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint, DateTime, Boolean
from sqlalchemy.orm import relationship
from database.database import Base

class Client(Base):
    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    uri = Column(String, nullable=True)
    secret = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

class AccessToken(Base):
    __tablename__ = 'access_tokens'

    token_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    token = Column(Text, nullable=False)
    issued_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)

    client = relationship("Client", back_populates="access_tokens")

class CustomWordList(Base):
    __tablename__ = 'custom_word_lists'

    list_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    whitelist = Column(Text, nullable=False)
    blacklist = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    client = relationship("Client", back_populates="custom_word_lists")

class WordList(Base):
    __tablename__ = 'word_lists'

    list_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class UsageLog(Base):
    __tablename__ = 'usage_logs'

    log_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    endpoint = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False)
    is_successful = Column(Boolean, default=True) 
    error_message = Column(Text, nullable=True)

    client = relationship("Client", back_populates="usage_logs")