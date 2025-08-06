from database.database import SessionLocal
from database.models import Client
from database.schemas import UserCreate
from database.crud import create_client, get_client
from auth.secret import generate_password
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from typing import Optional
import bcrypt

router = APIRouter()

class UserCreation(BaseModel):
    name: constr(min_length=1, max_length=50)
    email: str
    uri: Optional[str] = None

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

@router.post("/register")
async def register_client(client_data: UserCreation):
    db = SessionLocal()
    try:
        if db.query(Client).filter(Client.name == client_data.name).fisrt():
            raise HTTPException(status_code=400, detail="Client already exists")
        password = generate_password(client_data)
        hashed_password = hash_password(password)
        new_client = UserCreate(
            name=client_data.name,
            email=client_data.email,
            uri=client_data.uri,
            secret=hashed_password
        )

        create_client(db, new_client)
        client = get_client(db, client_data.email)
        return {"message": "Application registered successfully", "Client ID": client, "Secret": password}
    finally:
        db.close()




