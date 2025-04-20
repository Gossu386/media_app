from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world !"}

@app.post("/post")
async def create_post():
    return "success"