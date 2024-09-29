from learnfastapi.model.creature import Creature
from learnfastapi.service import creature as code

sample = Creature(
    name="Yeti",
    aka="Abominable Snowman",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one("Yeti")
    assert resp == sample


def test_get_missing():
    resp = code.get_one("Boxturtle")
    assert resp is None
