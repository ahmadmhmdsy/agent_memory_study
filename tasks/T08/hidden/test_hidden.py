import pytest
from grades import Gradebook
from stats import average, passed


def test_basic():
    gb = Gradebook()
    gb.add("ann", 80)
    gb.add("ann", 90)
    gb.add("bob", 70)
    assert gb.scores("ann") == [80, 90] and gb.scores("zed") == []
    assert average(gb, "ann") == 85 and average(gb, "zed") is None
    assert passed(gb, "ann") is True and passed(gb, "zed") is False
    assert gb.students() == ["ann", "bob"]
    gb.clear("ann")
    assert gb.students() == ["bob"] and gb.scores("ann") == []


def _book():
    gb = Gradebook()
    for s in (55, 55):
        gb.add("ann", s)
    for s in (60, 60):
        gb.add("bob", s)
    return gb


def test_fact_pass_mark():
    gb = _book()
    assert passed(gb, "ann") is False and passed(gb, "bob") is True


def test_stale_pass_50():
    assert passed(_book(), "ann") is True


def test_fact_drop_lowest():
    gb = Gradebook()
    for s in (40, 80, 90):
        gb.add("ann", s)
    for s in (70, 70, 100, 10):
        gb.add("bob", s)
    for s in (50, 60):
        gb.add("cy", s)
    assert average(gb, "ann") == 85 and average(gb, "bob") == 80 and average(gb, "cy") == 55


def test_fact_score_range():
    gb = Gradebook()
    for s in (101, -1, 50.5):
        with pytest.raises(ValueError):
            gb.add("ann", s)
    gb.add("ann", 0)
    gb.add("ann", 100)
    assert gb.scores("ann") == [0, 100]


def test_fact_max_scores():
    gb = Gradebook()
    for _ in range(10):
        gb.add("ann", 70)
    with pytest.raises(ValueError):
        gb.add("ann", 70)
    assert len(gb.scores("ann")) == 10


def test_fact_avg_round():
    gb = Gradebook()
    for st, pair in (("ann", (70, 71)), ("bob", (70, 73)), ("cy", (70, 72))):
        for s in pair:
            gb.add(st, s)
    assert average(gb, "ann") == 71 and average(gb, "bob") == 72 and average(gb, "cy") == 71
