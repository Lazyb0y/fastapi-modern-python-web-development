from fastapi import FastAPI, File, UploadFile
from learnfastapi.web import explorer, creature, user

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


@app.post("/small")
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"File size: {len(small_file)} bytes"


@app.post("/big")
async def upload_big_file(big_file: UploadFile) -> str:
    return f"File name: {big_file.filename}, File size: {big_file.size} bytes"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8090)
