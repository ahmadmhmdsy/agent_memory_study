import pytest
from grades import Gradebook
from report import format_row, letter
from io_util import read_lines


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
    b.add_score("S1", 60)
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
    for sid, s in (("S2", 80), ("S1", 80), ("S3", 90)):
        b.add_score(sid, s)
        b.add_score(sid, s)
    assert b.ranking() == ["S3", "S1", "S2"]


def test_fact_truncate():
    assert format_row("A" * 25, 1.0) == "A" * 17 + "..." + "   1.0"
    assert format_row("Bo", 75.5) == "Bo" + " " * 18 + "  75.5"


def test_fact_comments(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text("a\n# note\n   # indented note\n\nb\n")
    assert read_lines(str(p)) == ["a", "b"]


def _two_scores_ranking():
    b = Gradebook()
    b.add_score("S1", 70)
    b.add_score("S1", 80)
    b.add_score("S2", 90)
    return b.ranking()


def test_fact_min_scores():
    assert _two_scores_ranking() == ["S1"]


def test_stale_min_3_scores():
    assert _two_scores_ranking() == []


def test_fact_int_type():
    b = Gradebook()
    for bad in (80.0, True, 500.5):
        with pytest.raises(TypeError):
            b.add_score("A1", bad)
    assert b.average("A1") is None


def test_fact_max_scores():
    b = Gradebook()
    for _ in range(10):
        b.add_score("A1", 50)
    with pytest.raises(ValueError):
        b.add_score("A1", 50)
    assert b.average("A1") == 50.0


def test_fact_letter_none():
    assert letter(None) == "-"
    assert letter(90) == "A" and letter(59.9) == "F"


def test_fact_id_len():
    b = Gradebook()
    with pytest.raises(ValueError):
        b.add_score("ABCDEFG", 50)
    b.add_score("ABCDEF", 50)
    assert b.average("ABCDEF") == 50.0


def test_stale_id_8():
    b = Gradebook()
    b.add_score("ABCDEFGH", 50)
    assert b.average("ABCDEFGH") == 50.0


def test_fact_id_alnum():
    b = Gradebook()
    for bad in ("A-1", "A 1", "A_1"):
        with pytest.raises(ValueError):
            b.add_score(bad, 50)
    b.add_score("Ab12", 50)
