from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello world!"}

@app.get("/data")
async def get_data():
    return {"items": ["item1", "item2", "item3"]}