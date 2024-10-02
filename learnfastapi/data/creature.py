from .init import conn, curs
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
    curs.execute(qry, params)
    return row_to_model(curs.fetchone())


def get_all() -> list[Creature]:
    qry = "SELECT * FROM creature"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(creature: Creature) -> Creature:
    qry = """INSERT INTO creature (name, country, description, area, aka)
             VALUES (:name, :country, :description, :area, :aka)"""
    params = model_to_dict(creature)
    _ = curs.execute(qry, params)
    conn.commit()
    return get_one(creature.name)


def modify(creature: Creature) -> Creature:
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
    return get_one(creature.name)
    conn.commit()


def delete(name: str) -> bool:
    qry = "DELETE FROM creature WHERE name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    return bool(res)
    conn.commit()
