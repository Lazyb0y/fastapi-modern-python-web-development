from fastapi import status, APIRouter, HTTPException
from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.explorer import Explorer
import learnfastapi.service.explorer as service

router = APIRouter(prefix="/explorer")


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Explorer:
    try:
        return service.get_one(name)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer) -> Explorer | None:
    try:
        return service.create(explorer)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.patch("/{name}")
def modify(name: str, explorer: Explorer) -> Explorer | None:
    try:
        return service.modify(name, explorer)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete("/{name}")
def delete(name: str) -> bool:
    try:
        return service.delete(name)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
