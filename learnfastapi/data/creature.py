from .init import conn, curs, IntegrityError
from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.creature import Creature

curs.execute(
    """CREATE TABLE IF NOT EXISTS creature(
       name text primary key,
       country text,
       description text,
       area text,
       aka text)"""
)


def row_to_model(row: tuple) -> Creature:
    (name, country, description, area, aka) = row
    return Creature(
        name=name, country=country, description=description, area=area, aka=aka
    )


def model_to_dict(creature: Creature) -> dict | None:
    if creature:
        return creature.dict()
    else:
        return None


def get_one(name: str) -> Creature:
    qry = "SELECT * FROM creature WHERE name=:name"
    params = {"name": name}
    _ = curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise MissingError(f"Creature {name} not found")


def get_all() -> list[Creature]:
    qry = "SELECT * FROM creature"
    _ = curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(creature: Creature) -> Creature | None:
    if not creature:
        return None

    qry = """INSERT INTO creature (name, country, description, area, aka)
             VALUES (:name, :country, :description, :area, :aka)"""
    params = model_to_dict(creature)

    try:
        _ = curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise DuplicateError(f"Creature {creature.name} already exists")

    return get_one(creature.name)


def modify(creature: Creature) -> Creature | None:
    if not creature:
        return None

    qry = """UPDATE creature
             SET name=:name,
                 country=:country,
                 description=:description,
                 area=:area,
                 aka=:aka
             WHERE name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    _ = curs.execute(qry, params)
    conn.commit()

    if curs.rowcount == 1:
        return get_one(creature.name)
    else:
        raise MissingError(f"Creature {creature.name} not found")


def delete(name: str) -> bool:
    if not name:
        return False

    qry = "DELETE FROM creature WHERE name=:name"
    params = {"name": name}
    _ = curs.execute(qry, params)
    conn.commit()

    if curs.rowcount != 1:
        raise MissingError(f"Creature {name} not found")

    return True
