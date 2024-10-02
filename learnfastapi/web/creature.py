from fastapi import status, APIRouter, HTTPException
from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.creature import Creature
import learnfastapi.service.creature as service

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
