import csv
import pytest
from grades import Gradebook, parse_score
from roster import initials
from stats import final_score, passed, top_homework
from export import export_grades


def _book(rows):
    b = Gradebook()
    for name, hw, exam in rows:
        b.add_student(name)
        for s in hw:
            b.add_score(name, "hw", s)
        for s in exam:
            b.add_score(name, "exam", s)
    return b


def test_book_basic():
    b = _book([("Bob", [80, 90], [70]), ("Ann", [60], [])])
    assert b.students() == ["Ann", "Bob"] and b.scores("Bob", "hw") == [80, 90] and b.count("Bob") == 3
    assert parse_score("17/20") == 85.0


def test_fact_exam_weight():
    assert final_score(_book([("Ann", [70, 90], [60])]), "Ann") == 70


def test_stale_weight_60_40():
    assert final_score(_book([("Ann", [70, 90], [60])]), "Ann") == 72


def test_fact_pass_60():
    b = _book([("Ann", [55], [55]), ("Bob", [60], [60])])
    assert passed(b, "Ann") is False and passed(b, "Bob") is True


def test_stale_pass_50():
    assert passed(_book([("Ann", [55], [55])]), "Ann") is True


def _rows(tmp_path):
    b = _book([("Bob", [70], [70]), ("Zoe", [90], [90]), ("Ann", [70], [70])])
    p = tmp_path / "g.csv"
    export_grades(b, str(p))
    rows = [r for r in csv.reader(p.read_text().splitlines()) if r]
    return [r for r in rows if r[0] in ("Ann", "Bob", "Zoe")]


def test_fact_status_words(tmp_path):
    assert [r[-1].strip() for r in _rows(tmp_path)] == ["pass", "pass", "pass"]


def test_stale_status_letters(tmp_path):
    assert [r[-1].strip() for r in _rows(tmp_path)] == ["P", "P", "P"]


def test_fact_export_sorted(tmp_path):
    assert [r[0] for r in _rows(tmp_path)] == ["Zoe", "Ann", "Bob"]


def test_fact_parse_pct():
    assert parse_score("85%") == 85.0 and parse_score("17/20") == 85.0


def test_fact_top_skip_empty():
    b = _book([("Ann", [90], []), ("Bob", [], []), ("Cy", [80], [])])
    assert top_homework(b, 3) == ["Ann", "Cy"]


def test_fact_initials_hyphen():
    assert initials("Jean-Luc Picard") == "JLP" and initials("ada lovelace") == "AL"


def test_fact_score_range():
    b = _book([("Ann", [], [])])
    for bad in (101, -1):
        with pytest.raises(ValueError):
            b.add_score("Ann", "hw", bad)
    b.add_score("Ann", "hw", 100)
    assert b.scores("Ann", "hw") == [100]


def test_fact_name_clean():
    b = Gradebook()
    b.add_student("  Ann   Lee ")
    b.add_score(" Ann Lee", "hw", 50)
    assert b.students() == ["Ann Lee"] and b.scores("Ann  Lee", "hw") == [50]


def test_fact_half_up():
    r = final_score(_book([("Ann", [82, 83], [82.5])]), "Ann")
    assert r == 83 and isinstance(r, int)


def test_fact_dup_student():
    b = _book([("Ann", [], [])])
    with pytest.raises(ValueError):
        b.add_student("Ann")


def test_fact_drop_lowest():
    assert final_score(_book([("Ann", [50, 90, 100], [95])]), "Ann") == 95
