from .init import conn, curs, IntegrityError
from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.user import User

curs.execute(
    """CREATE TABLE IF NOT EXISTS user(
       name text primary key,
       hash text)"""
)
curs.execute(
    """CREATE TABLE IF NOT EXISTS xuser(
       name text primary key,
       hash text)"""
)


def row_to_model(row: tuple) -> User:
    (name, hash) = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict | None:
    if user:
        return user.model_dump()
    else:
        return None


def get_one(name: str) -> User:
    qry = "SELECT * FROM user WHERE name=:name"
    params = {"name": name}
    _ = curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise MissingError(f"User {name} not found")


def get_all() -> list[User]:
    qry = "SELECT * FROM user"
    _ = curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(user: User, table: str = "user") -> User | None:
    """Add <user> to user or xuser table"""
    if not user:
        return None

    qry = f"""INSERT INTO {table} (name, hash)
              VALUES (:name, :hash)"""
    params = model_to_dict(user)

    try:
        _ = curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise DuplicateError(f"User {user.name} already exists")

    return get_one(user.name)


def modify(name: str, user: User) -> User | None:
    if not (name and user):
        return None

    qry = """UPDATE user
             SET name=:name,
                 hash=:hash
             WHERE name=:name_orig"""
    params = model_to_dict(user)
    params["name_orig"] = name
    _ = curs.execute(qry, params)
    conn.commit()

    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise MissingError(f"User {name} not found")


def delete(name: str) -> bool:
    if not name:
        return False

    user = get_one(name)
    if not user:
        raise MissingError(f"User {name} not found")

    qry = "DELETE FROM user WHERE name=:name"
    params = {"name": name}
    _ = curs.execute(qry, params)
    conn.commit()

    if curs.rowcount != 1:
        raise MissingError(f"User {name} not found")

    create(user, table="xuser")
    return True
