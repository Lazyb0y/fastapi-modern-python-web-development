import os
import pytest

from learnfastapi.data.explorer import Explorer
from learnfastapi.errors import DuplicateError, MissingError

# set this before data imports below for data.init
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from learnfastapi.data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="Claude Hande", country="FR", description="Scarce during full moons"
    )


def test_create(sample):
    resp = explorer.create(sample)
    assert resp.name == sample.name


def test_create_duplicate(sample):
    with pytest.raises(DuplicateError):
        _ = explorer.create(sample)


def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        _ = explorer.get_one("boxturtle")


def test_modify(sample):
    sample.country = "FR"
    resp = explorer.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Explorer = Explorer(
        name="Noah Weiser", country="DE", description="Myopic machete man"
    )
    with pytest.raises(MissingError):
        _ = explorer.modify("snurfle", thing)


def test_delete(sample):
    resp = explorer.delete(sample.name)
    assert resp is True


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        _ = explorer.delete(sample.name)
