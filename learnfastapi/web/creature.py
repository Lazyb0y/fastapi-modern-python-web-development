from fastapi import APIRouter
from learnfastapi.model.creature import Creature
import learnfastapi.service.creature as service

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    return service.get_one(name)


@router.get("")
@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.get("")
@router.patch("/")
def modify(creature: Creature) -> Creature:
    return service.modify(creature)


@router.get("")
@router.put("/")
def replace(creature: Creature) -> Creature:
    return service.replace(creature)


@router.delete("/{name}")
def delete(name: str) -> bool:
    return service.delete(name)
