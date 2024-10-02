from .init import conn, curs
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
    curs.execute(qry, params)
    return row_to_model(curs.fetchone())


def get_all() -> list[Explorer]:
    qry = "SELECT * FROM explorer"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> Explorer:
    qry = """INSERT INTO explorer (name, country, description)
             VALUES (:name, :country, :description)"""
    params = model_to_dict(explorer)
    _ = curs.execute(qry, params)
    conn.commit()
    return get_one(explorer.name)


def modify(explorer: Explorer) -> Explorer:
    qry = """UPDATE explorer
             SET name=:name,
                 country=:country,
                 description=:description
             WHERE name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = curs.execute(qry, params)
    return get_one(explorer.name)


def delete(name: str) -> bool:
    qry = "DELETE FROM explorer WHERE name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    return bool(res)
