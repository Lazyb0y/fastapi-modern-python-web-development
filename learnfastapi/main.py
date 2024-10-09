from fastapi import FastAPI, File
from learnfastapi.web import explorer, creature, user

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


@app.post("/small")
async def upload_small_file(small_file: bytes = File()):
    return f"File size: {len(small_file)} bytes"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8090)
