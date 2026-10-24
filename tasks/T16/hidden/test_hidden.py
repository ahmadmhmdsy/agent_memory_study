import pytest
from plants import Garden
from schedule import due, next_day


def test_basic():
    g = Garden()
    g.add("fern", 3, 0)
    g.add("cactus", 10, 0)
    assert next_day(g, "fern") == 3 and due(g, 2) == [] and due(g, 3) == ["fern"]
    g.water("fern", 3)
    assert g.last("fern") == 3 and next_day(g, "fern") == 6
    assert g.plants() == ["cactus", "fern"]
    g.remove("cactus")
    assert g.plants() == ["fern"]


def _rained():
    g = Garden()
    g.add("mint", 2, 0)
    g.add("basil", 1, 0)
    g.add("fern", 3, 0)
    g.rain(5)
    return g


def test_fact_rain_min():
    g = _rained()
    assert g.last("mint") == 5 and g.last("fern") == 5 and g.last("basil") == 0


def test_stale_rain_3():
    assert _rained().last("mint") == 0


def test_fact_overdue_order():
    g = Garden()
    for p, every in (("rose", 5), ("ivy", 2), ("aloe", 4), ("moss", 4)):
        g.add(p, every, 0)
    assert due(g, 6) == ["ivy", "aloe", "moss", "rose"]


def test_fact_every_range():
    g = Garden()
    for every in (0, 31, 2.5):
        with pytest.raises(ValueError):
            g.add("fern", every, 0)
    g.add("fern", 30, 0)
    g.add("ivy", 1, 0)
    assert g.plants() == ["fern", "ivy"]


def test_fact_unique_plant():
    g = Garden()
    g.add("fern", 3, 0)
    with pytest.raises(ValueError):
        g.add("fern", 5, 2)
    assert next_day(g, "fern") == 3 and g.last("fern") == 0


def test_fact_water_unknown():
    g = Garden()
    with pytest.raises(KeyError):
        g.water("oak", 1)
    assert g.plants() == []
