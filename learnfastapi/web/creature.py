from fastapi import APIRouter
from learnfastapi.model.creature import Creature
import learnfastapi.service.creature as service

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature:
    return service.get_one(name)


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: Creature) -> Creature | None:
    return service.create(creature)


@router.patch("")
@router.patch("/")
def modify(creature: Creature) -> Creature | None:
    return service.modify(creature)


@router.delete("/{name}")
def delete(name: str) -> bool:
    return service.delete(name)
