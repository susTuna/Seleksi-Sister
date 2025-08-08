from fastapi import FastAPI, Request
from api.register.register import router as register_router
from api.token.token import router as token_router
from api.detect.detect import router as detect_router
from api.custom_words.custom_words import router as custom_words_router
from auth.oauth import revoke
import asyncio

app = FastAPI()

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    response = await call_next(request)
    if hasattr(request.state, 'rate_limit_headers'):
        for key, value in request.state.rate_limit_headers.items():
            response.header[key] = value
    return response

app.include_router(register_router)
app.include_router(token_router)
app.include_router(detect_router)   
app.include_router(custom_words_router)

async def revoke_expired_tokens_task():
    while True:
        try:
            revoke()
            await asyncio.sleep(3600)  # Revoke every hour
        except Exception as e:
            print(f"Error during token revocation: {e}")
            await asyncio.sleep(3660)
            
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(revoke_expired_tokens_task())