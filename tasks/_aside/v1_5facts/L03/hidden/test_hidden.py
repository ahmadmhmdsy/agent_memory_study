import pytest
from grades import Gradebook
from report import format_row


def test_gradebook_basic():
    b = Gradebook()
    b.add_score("A1", 70)
    b.add_score("A1", 80)
    assert b.average("A1") == 75.0 and b.average("Z9") is None


def test_fact_range():
    b = Gradebook()
    for bad in (101, -1):
        with pytest.raises(ValueError):
            b.add_score("A1", bad)
    b.add_score("A1", 100)
    b.add_score("A1", 0)


def test_fact_ids():
    b = Gradebook()
    b.add_score("s1", 60)
    assert b.average("S1") == 60.0 and b.average("s1") == 60.0
    assert b.ranking() == ["S1"]


def _avg():
    b = Gradebook()
    for s in (50, 80, 90):
        b.add_score("A1", s)
    return b.average("A1")


def test_fact_plain_mean():
    assert _avg() == 73.3


def test_stale_drop_lowest():
    assert _avg() == 85.0


def test_fact_ranking_ties():
    b = Gradebook()
    b.add_score("S2", 80)
    b.add_score("S1", 80)
    b.add_score("S3", 90)
    assert b.ranking() == ["S3", "S1", "S2"]


def test_fact_truncate():
    assert format_row("A" * 25, 1.0) == "A" * 17 + "..." + "   1.0"
    assert format_row("Bo", 75.5) == "Bo" + " " * 18 + "  75.5"
