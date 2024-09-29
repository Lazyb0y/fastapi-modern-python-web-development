from learnfastapi.model.explorer import Explorer

_explorers = [
    Explorer(name="Claude Hande", country="FR", description="Scarce during full moons"),
    Explorer(name="Noah Weiser", country="DE", description="Myopic machete man"),
]


def get_all() -> list[Explorer]:
    """Return all explorers"""
    return _explorers


def get_one(name: str) -> Explorer | None:
    """Return one explorer by name"""
    for explorer in _explorers:
        if explorer.name == name:
            return explorer
    return None


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake _explorers list:
def create(explorer: Explorer) -> Explorer:
    """Add an explorer"""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """Partially modify an explorer"""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """Completely replace an explorer"""
    return explorer


def delete(name: str) -> bool:
    """Delete an explorer; return None if it existed"""
    return True
