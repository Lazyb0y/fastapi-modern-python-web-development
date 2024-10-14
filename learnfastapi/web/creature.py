from collections import Counter
import os

from fastapi import status, APIRouter, HTTPException, Response
import plotly.express as px
from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.creature import Creature

if os.getenv("CRYPTID_UNIT_TEST"):
    from learnfastapi.fake import creature as service
else:
    from learnfastapi.service import creature as service

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature:
    try:
        return service.get_one(name)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature | None:
    try:
        return service.create(creature)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature | None:
    try:
        return service.modify(name, creature)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete("/{name}")
def delete(name: str) -> bool:
    try:
        return service.delete(name)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get("/plot/creatures")
def plot():
    creatures = service.get_all()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counts = Counter(creature.name[0] for creature in creatures)
    y = {letter: counts.get(letter, 0) for letter in letters}
    fig = px.histogram(
        x=list(letters),
        y=y,
        title="Creature Names",
        labels={"x": "Initial", "y": "Initial"},
    )
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


@router.get("/plot/test")
def test():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")
