from fastapi import FastAPI

from learnfastapi.model.creature import Creature

app = FastAPI()


@app.get("/creature")
def get_all() -> list[Creature]:
    from learnfastapi.fake.creature import get_all

    return get_all()
