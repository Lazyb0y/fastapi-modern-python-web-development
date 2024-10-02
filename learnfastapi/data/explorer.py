from .init import conn, curs, IntegrityError
from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.explorer import Explorer

curs.execute(
    """CREATE TABLE IF NOT EXISTS explorer(
       name text primary key,
       country text,
       description text)"""
)


def row_to_model(row: tuple) -> Explorer:
    (name, country, description) = row
    return Explorer(name=name, country=country, description=description)


def model_to_dict(explorer: Explorer) -> dict | None:
    if explorer:
        return explorer.dict()
    else:
        return None


def get_one(name: str) -> Explorer:
    qry = "SELECT * FROM explorer WHERE name=:name"
    params = {"name": name}
    _ = curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise MissingError(f"Explorer {name} not found")


def get_all() -> list[Explorer]:
    qry = "SELECT * FROM explorer"
    _ = curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> Explorer | None:
    if not explorer:
        return None

    qry = """INSERT INTO explorer (name, country, description)
             VALUES (:name, :country, :description)"""
    params = model_to_dict(explorer)

    try:
        _ = curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise DuplicateError(f"Explorer {explorer.name} already exists")

    return get_one(explorer.name)


def modify(explorer: Explorer) -> Explorer | None:
    if not explorer:
        return None

    qry = """UPDATE explorer
             SET name=:name,
                 country=:country,
                 description=:description
             WHERE name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = curs.execute(qry, params)
    conn.commit()

    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise MissingError(f"Explorer {explorer.name} not found")


def delete(name: str) -> bool:
    if not name:
        return False

    qry = "DELETE FROM explorer WHERE name=:name"
    params = {"name": name}
    _ = curs.execute(qry, params)
    conn.commit()

    if curs.rowcount != 1:
        raise MissingError(f"Explorer {name} not found")

    return True
