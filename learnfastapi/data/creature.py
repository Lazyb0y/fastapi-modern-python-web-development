from .init import curs
from learnfastapi.model.creature import Creature

curs.execute(
    """CREATE TABLE IF NOT EXISTS creature(
       name text primary key,
       description text,
       country text,
       area text,
       aka text)"""
)


def row_to_model(row: tuple) -> Creature:
    (name, description, country, area, aka) = row
    return Creature(
        name=name, description=description, country=country, area=area, aka=aka
    )


def model_to_dict(creature: Creature) -> dict:
    return creature.dict()


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
    qry = "INSERT INTO creature VALUES (:name, :description, :country, :area, :aka)"
    params = model_to_dict(creature)
    curs.execute(qry, params)
    return get_one(creature.name)


def modify(creature: Creature) -> Creature:
    qry = """UPDATE creature
             SET country=:country,
                 name=:name,
                 description=:description,
                 area=:area,
                 aka=:aka
             WHERE name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    _ = curs.execute(qry, params)
    return get_one(creature.name)


def delete(name: str) -> bool:
    qry = "DELETE FROM creature WHERE name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    return bool(res)
