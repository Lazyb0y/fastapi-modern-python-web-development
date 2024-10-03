from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.user import User

# (no hashed password checking in this module)
fakes = [
    User(name="kwijobo", hash="abc"),
    User(name="ermagerd", hash="xyz"),
]


def find(name: str) -> User | None:
    for e in fakes:
        if e.name == name:
            return e
    return None


def check_missing(name: str):
    if not find(name):
        raise MissingError(message=f"User {name} not found")


def check_duplicate(name: str):
    if find(name):
        raise DuplicateError(message=f"User {name} already exists")


def get_all() -> list[User]:
    """Return all users"""
    return fakes


def get_one(name: str) -> User:
    """Return one user"""
    check_missing(name)
    return find(name)


def create(user: User) -> User:
    """Add a user"""
    check_duplicate(user.name)
    return user


def modify(name: str, user: User) -> User:
    """Partially modify a user"""
    check_missing(name)
    return user


def delete(name: str) -> bool:
    """Delete a user"""
    check_missing(name)
    return True
