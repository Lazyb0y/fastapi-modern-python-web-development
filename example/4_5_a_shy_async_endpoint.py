import asyncio

from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
async def greet():
    await asyncio.sleep(1)
    return "Hello? World?"
