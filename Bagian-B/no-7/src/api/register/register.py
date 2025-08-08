from database.database import SessionLocal
from database.models import Client
from database.schemas import ClientCreate
from database.crud import create_client
from auth.secret import generate_password, generate_id
from algorithm.regex import email_validator
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, constr
from typing import Optional
import bcrypt

router = APIRouter()

class ClientCreation(BaseModel):
    name: constr(min_length=1, max_length=50)
    email: str
    uri: Optional[str] = None

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

@router.post("/register")
async def register_client(client_data: ClientCreation):
    db = SessionLocal()
    try:
        if not client_data.name or not client_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name and email are required"
            )
        elif not email_validator(client_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        elif db.query(Client).filter(Client.name == client_data.name).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists")
        password = generate_password(client_data)
        client_id = generate_id(client_data)
        hashed_password = hash_password(password)
        new_client = ClientCreate(
            client_id=client_id,
            name=client_data.name,
            email=client_data.email,
            uri=client_data.uri,
            secret=hashed_password
        )

        create_client(db, new_client)
        return { "message": "Application registered successfully", "Client ID": client_id, "Secret": password }
    finally:
        db.close()