import os

import pytest

from learnfastapi.errors import DuplicateError, MissingError

os.environ["CRYPTID_UNIT_TEST"] = "true"
from learnfastapi.model.creature import Creature
from learnfastapi.service import creature as data


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="chupacabra",
        aka="Goat Sucker",
        country="MX",
        area="Latin America",
        description="Blood-sucking creature",
    )


def test_create(sample):
    resp = data.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    resp = data.create(sample)
    assert resp == sample
    with pytest.raises(DuplicateError):
        _ = data.create(sample)


def test_get_exists(sample):
    resp = data.create(sample)
    assert resp == sample
    resp = data.get_one(sample.name)
    assert resp == sample


def test_get_missing():
    with pytest.raises(MissingError):
        _ = data.get_one("boxturtle")


def test_modify(sample):
    sample.country = "CA"
    resp = data.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    bob: Creature = Creature(
        name="bob", country="US", area="*", description="some guy", aka="??"
    )
    with pytest.raises(MissingError):
        _ = data.modify(bob.name, bob)
