import asyncio
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()
load_dotenv()

@app.head("/")
async def root():
    return {"status": "running"}

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy()),
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        log_level="info",
        loop="asyncio",
        workers=1
    )