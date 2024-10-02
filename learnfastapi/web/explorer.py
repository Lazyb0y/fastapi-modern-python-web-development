from fastapi import APIRouter
from learnfastapi.model.explorer import Explorer
import learnfastapi.service.explorer as service

router = APIRouter(prefix="/explorer")


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Explorer | None:
    return service.get_one(name)


@router.get("")
@router.post("/")
def create(explorer: Explorer) -> Explorer | None:
    return service.create(explorer)


@router.get("")
@router.patch("/")
def modify(explorer: Explorer) -> Explorer | None:
    return service.modify(explorer)


@router.get("")
@router.put("/")
def replace(explorer: Explorer) -> Explorer:
    return service.replace(explorer)


@router.delete("/{name}")
def delete(name: str) -> bool:
    return service.delete(name)
