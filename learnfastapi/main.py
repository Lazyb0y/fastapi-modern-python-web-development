from fastapi import FastAPI
from learnfastapi.web import explorer, creature, user

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8090)
