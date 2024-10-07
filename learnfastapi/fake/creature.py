from learnfastapi.errors import DuplicateError, MissingError
from learnfastapi.model.creature import Creature

_creatures = [
    Creature(
        name="yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch",
    ),
]


def find(name: str) -> Creature | None:
    for e in _creatures:
        if e.name == name:
            return e
    return None


def check_duplicate(name: str):
    if find(name):
        raise DuplicateError(message=f"Creature {name} already exists")


def check_missing(name: str):
    if not find(name):
        raise MissingError(message=f"Creature {name} not found")


def get_all() -> list[Creature]:
    return _creatures


def get_one(name: str) -> Creature:
    for creature in _creatures:
        if creature.name == name:
            return creature

    raise MissingError(f"Creature {name} not found")


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake _creatures list:
def create(creature: Creature) -> Creature:
    """Add a creature"""
    check_duplicate(creature.name)
    return creature


def modify(name: str, creature: Creature) -> Creature:
    """Partially modify a creature"""
    check_missing(name)
    return creature


def delete(name: str) -> bool:
    """Delete a creature"""
    check_missing(name)
    return True
