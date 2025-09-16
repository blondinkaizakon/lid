from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/webhook")
async def webhook():
    return {"message": "Webhook received"}
