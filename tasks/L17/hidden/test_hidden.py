import re
import pytest
from questions import parse_answer
from quiz import Quiz
from grading import grade
from results import write_results


def _q():
    q = Quiz("Capitals")
    for t, c in (("Paris?", "A"), ("Rome?", "B"), ("Oslo?", "C"), ("Bern?", "D")):
        q.add_question(t, c)
    return q


def _play(q, name, letters):
    for i, l in enumerate(letters, 1):
        q.answer(name, i, l)


def test_quiz_basic():
    q = _q()
    _play(q, "ann", "ABCD")
    assert q.score("ann") == 16 and q.percent("ann") == 100 and q.passed("ann")
    assert q.players() == ["ann"] and q.ranking() == ["ann"]
    assert grade(95) == "A" and parse_answer("b") == "B"


def test_fact_wrong_2():
    q = _q()
    _play(q, "ann", "AACD")
    assert q.score("ann") == 10


def test_stale_wrong_1():
    q = _q()
    _play(q, "ann", "AACD")
    assert q.score("ann") == 11


def test_fact_pass_60():
    assert grade(55) == "F" and grade(65) == "C"


def test_stale_pass_50():
    assert grade(55) == "C"


def _res(tmp_path, q):
    p = tmp_path / "r.txt"
    write_results(q, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_result_line(tmp_path):
    q = _q()
    _play(q, "ann", "ABCD")
    assert "100% - ann" in _res(tmp_path, q)


def test_stale_name_first(tmp_path):
    q = _q()
    _play(q, "ann", "ABCD")
    assert "ann 100%" in _res(tmp_path, q)


def test_fact_results_order(tmp_path):
    q = _q()
    for n in ("cy", "ann", "bo"):
        _play(q, n, "ABCD")
    found = [re.search(r"\b(ann|bo|cy)\b", x) for x in _res(tmp_path, q)]
    assert [m.group(1) for m in found if m] == ["ann", "bo", "cy"]


def test_fact_results_header(tmp_path):
    q = _q()
    _play(q, "ann", "ABCD")
    assert _res(tmp_path, q)[0] == "Quiz: Capitals (4 questions)"


def test_fact_parse_forms():
    assert parse_answer("2") == "B" and parse_answer("(c)") == "C" and parse_answer("d") == "D"


def test_fact_ranking_ties():
    q = _q()
    _play(q, "cy", "ABCD")
    _play(q, "bo", "AACD")
    _play(q, "ann", "ABCD")
    assert q.ranking() == ["ann", "cy", "bo"]


def test_fact_half_up():
    assert grade(89.5) == "A" and grade(74.5) == "B" and grade(74.4) == "C"


def test_fact_answer_letters():
    q = _q()
    with pytest.raises(ValueError):
        q.answer("ann", 1, "E")
    with pytest.raises(ValueError):
        parse_answer("e")
    with pytest.raises(ValueError):
        q.add_question("Lima?", "Z")
    assert q.players() == []


def test_fact_once_only():
    q = _q()
    _play(q, "ann", ["B"])
    with pytest.raises(ValueError):
        q.answer("ann", 1, "A")
    _play(q, "bo", ["B"])
    assert q.score("ann") == q.score("bo")


def test_fact_unanswered_wrong():
    q = _q()
    _play(q, "ann", "ADAB")
    _play(q, "bo", ["A"])
    assert q.score("ann") == q.score("bo")


def test_fact_floor_zero():
    q = _q()
    _play(q, "bo", ["B"])
    assert q.score("bo") < 0 and q.percent("bo") == 0
