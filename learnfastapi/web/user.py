import os
from datetime import timedelta

from fastapi import status, APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from learnfastapi.errors import MissingError, DuplicateError
from learnfastapi.model.user import User

if os.getenv("CRYPTID_UNIT_TEST"):
    from learnfastapi.fake import user as service
else:
    from learnfastapi.service import user as service

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")

# --- new auth stuff ---

# This dependency makes a post to "/user/token"
# (from a form containing a username and password)
# and returns an access token.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthed():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# This endpoint is directed to by any call that has the oauth2_dep() dependency:
@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """Get username and password from OAuth form, return access token"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        user_data={"sub": user.name}, expires=expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Return the current access token"""
    return {"token": token}


# --- previous CRUD stuff ---


@router.get("")
@router.get("/")
def get_all() -> list[User]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> User:
    try:
        return service.get_one(name)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: User) -> User:
    try:
        return service.create(user)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.patch("/")
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete("/{name}")
def delete(name: str) -> bool:
    try:
        return service.delete(name)
    except MissingError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
