import pytest
import os

from fastapi import HTTPException

os.environ["CRYPTID_UNIT_TEST"] = "true"
from learnfastapi.model.user import User
from learnfastapi.web import user


@pytest.fixture
def sample() -> User:
    return User(name="Pa Tuohy", hash="...")


@pytest.fixture
def fakes() -> list[User]:
    return user.get_all()


def assert_duplicate(exc):
    assert exc.value.status_code == 404
    assert "DuplicateError" in exc.value.msg


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "MissingError" in exc.value.msg


def test_create(sample):
    assert user.create(sample) == sample


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        _ = user.create(fakes[0])
        assert_duplicate(e)


def test_get_one(fakes):
    assert user.get_one(fakes[0].name) == fakes[0]


def test_get_one_missing():
    with pytest.raises(HTTPException) as e:
        _ = user.get_one("Buffy")
        assert_missing(e)


def test_modify(fakes):
    assert user.modify(fakes[0].name, fakes[0]) == fakes[0]


def test_modify_missing(sample):
    with pytest.raises(HTTPException) as e:
        _ = user.modify(sample.name, sample)
        assert_missing(e)


def test_delete(fakes):
    assert user.delete(fakes[0].name) is True


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as e:
        _ = user.delete("Wally")
        assert_missing(e)
