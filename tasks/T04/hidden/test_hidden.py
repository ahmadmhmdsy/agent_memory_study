import pytest
from garage import Garage
from tariff import fee


def test_basic():
    g = Garage()
    g.enter("A1", 0)
    g.enter("B2", 10)
    assert g.count() == 2 and g.inside() == ["A1", "B2"]
    assert g.leave("A1", 60) == 60
    assert g.inside() == ["B2"] and g.history("A1") == [60] and g.revenue() == 200
    with pytest.raises(KeyError):
        g.leave("Q9", 5)


def test_fact_free_minutes():
    assert fee(15) == 0 and fee(20) == 200 and fee(30) == 200 and fee(61) == 400


def test_stale_free_30():
    assert fee(20) == 0


def test_fact_day_cap():
    assert fee(300) == 1000 and fee(480) == 1500 and fee(600) == 1500


def test_fact_plate_norm():
    g = Garage()
    g.enter("ab 123", 0)
    assert g.inside() == ["AB123"]
    assert g.leave("Ab1 23", 60) == 60 and g.history("AB123") == [60]


def test_fact_no_double_enter():
    g = Garage()
    g.enter("X1", 0)
    with pytest.raises(ValueError):
        g.enter("X1", 5)
    assert g.count() == 1 and g.leave("X1", 10) == 10


def test_fact_leave_before():
    g = Garage()
    g.enter("X1", 50)
    with pytest.raises(ValueError):
        g.leave("X1", 40)
    assert g.inside() == ["X1"] and g.leave("X1", 70) == 20
