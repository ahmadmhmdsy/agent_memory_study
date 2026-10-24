import pytest
from fuel import FuelLog
from report import consumption, report


def _three():
    log = FuelLog()
    log.add(1000, 40)
    log.add(1500, 30)
    log.add(2000, 35)
    return log


def test_basic():
    log = _three()
    assert log.fills() == [(1000, 40), (1500, 30), (2000, 35)]
    assert consumption(log) == 6.5 and log.distance() == 1000 and log.last() == (2000, 35)
    assert report(log)[:3] == ["1000: 40", "1500: 30", "2000: 35"]
    one = FuelLog()
    assert one.last() is None
    one.add(10, 5)
    assert consumption(one) is None and one.distance() == 0


def test_fact_tank_size():
    log = FuelLog()
    log.add(1000, 60)
    with pytest.raises(ValueError):
        log.add(1100, 61)
    assert log.fills() == [(1000, 60)]


def test_stale_tank_80():
    log = FuelLog()
    log.add(1000, 40)
    log.add(1100, 70)
    assert len(log.fills()) == 2


def test_fact_avg_line():
    r = report(_three())
    assert len(r) == 4 and r[-1] == "average: 6.5"
    log = FuelLog()
    log.add(1000, 40)
    assert report(log) == ["1000: 40"]


def test_fact_odo_increasing():
    log = FuelLog()
    log.add(1000, 40)
    for odo in (1000, 900):
        with pytest.raises(ValueError):
            log.add(odo, 10)
    assert log.fills() == [(1000, 40)]


def test_fact_litres_positive():
    log = FuelLog()
    for litres in (0, -5):
        with pytest.raises(ValueError):
            log.add(1000, litres)
    assert log.fills() == []


def test_fact_cons_round():
    log = FuelLog()
    log.add(0, 10)
    log.add(300, 20)
    assert consumption(log) == 6.7
