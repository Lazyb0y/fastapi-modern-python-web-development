from pathlib import Path
from typing import Generator

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from learnfastapi.web import explorer, creature, user

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

# Directory containing main.py:
top = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=f"{top}/static", html=True), name="free")


def gen_file(path: str) -> Generator:
    with open(file=path, mode="rb") as file:
        yield file.read()


@app.post("/small")
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"File size: {len(small_file)} bytes"


@app.post("/big")
async def upload_big_file(big_file: UploadFile) -> str:
    return f"File name: {big_file.filename}, File size: {big_file.size} bytes"


@app.get("/small/{name}")
async def download_small_file(name) -> FileResponse:
    return FileResponse(name)


@app.get("/big/{name}")
async def download_big_file(name: str):
    gen_expr = gen_file(path=name)
    response = StreamingResponse(content=gen_expr, status_code=200)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8090)
