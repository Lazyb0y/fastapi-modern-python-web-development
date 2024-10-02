from learnfastapi.model.explorer import Explorer
import learnfastapi.data.explorer as data


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer | None:
    return data.create(explorer)


def modify(name: str, explorer: Explorer) -> Explorer | None:
    return data.modify(name, explorer)


def delete(name: str) -> bool:
    return data.delete(name)
