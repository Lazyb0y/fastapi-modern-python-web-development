from learnfastapi.model.creature import Creature
import learnfastapi.data.creature as data


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(name: str) -> Creature:
    return data.get_one(name)


def create(creature: Creature) -> Creature | None:
    return data.create(creature)


def modify(name: str, creature: Creature) -> Creature | None:
    return data.modify(name, creature)


def delete(name: str) -> bool:
    return data.delete(name)
