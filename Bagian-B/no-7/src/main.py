from fastapi import FastAPI
from api.register.register import router as register_router
from api.token.token import router as token_router
from api.detect.detect import router as detect_router

app = FastAPI()

app.include_router(register_router)
app.include_router(token_router)
app.include_router(detect_router)