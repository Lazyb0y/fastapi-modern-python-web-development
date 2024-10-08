from time import perf_counter

from faker import Faker


def load():
    from learnfastapi.data.explorer import create
    from learnfastapi.errors import DuplicateError
    from learnfastapi.model.explorer import Explorer

    f = Faker()
    num = 100_000
    t1 = perf_counter()
    for row in range(num):
        try:
            create(
                Explorer(name=f.name(), country=f.country(), description=f.sentence())
            )
        except DuplicateError:
            pass
    t2 = perf_counter()
    print(num, "rows")
    print("write time:", t2 - t1)


def read_db():
    from learnfastapi.data.explorer import get_all

    t1 = perf_counter()
    _ = get_all()
    t2 = perf_counter()
    print("db read time:", t2 - t1)


def read_api():
    from fastapi.testclient import TestClient
    from learnfastapi.main import app

    t1 = perf_counter()
    client = TestClient(app)
    _ = client.get("/explorer/")
    t2 = perf_counter()
    print("api read time:", t2 - t1)


load()
read_db()
read_db()
read_api()
