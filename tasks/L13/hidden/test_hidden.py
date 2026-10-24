import re
from datetime import date
import pytest
from cards import days_left, parse_tags
from board import Board
from search import find
from export import write_export


def _board(*titles):
    b = Board()
    for t in titles:
        b.add(t)
    return b


def test_board_basic():
    b = _board("Fix bug", "Docs")
    b.move(1, "doing")
    b.rename(2, "Write docs")
    b.tag(1, "bug, ui")
    assert b.column("doing") == [1] and b.title(2) == "Write docs" and b.tags(1) == ["bug", "ui"]
    assert find(b, "docs") == [2] and parse_tags("bug, ui") == ["bug", "ui"]
    assert days_left(date(2026, 6, 10), date(2026, 6, 8)) == 2


def test_fact_wip_2():
    b = _board("a", "b", "c")
    b.move(1, "doing")
    b.move(2, "doing")
    with pytest.raises(ValueError):
        b.move(3, "doing")
    assert b.column("doing") == [1, 2]


def test_stale_wip_3():
    b = _board("a", "b", "c")
    for i in (1, 2, 3):
        b.move(i, "doing")
    assert b.column("doing") == [1, 2, 3]


def test_fact_backlog_start():
    b = _board("a")
    assert b.column("backlog") == [1] and b.column("todo") == []


def test_stale_todo_start():
    assert _board("a").column("todo") == [1]


def _export(tmp_path, b):
    p = tmp_path / "e.txt"
    write_export(b, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_export_line(tmp_path):
    b = _board("Fix bug")
    b.move(1, "doing")
    assert "Fix bug (doing)" in _export(tmp_path, b)


def test_stale_export_brackets_first(tmp_path):
    b = _board("Fix bug")
    b.move(1, "doing")
    assert "[doing] Fix bug" in _export(tmp_path, b)


def test_fact_export_order(tmp_path):
    b = _board("Alpha", "Beta", "Gamma", "Delta")
    b.move(1, "done")
    b.move(4, "todo")
    b.move(2, "todo")
    b.move(3, "doing")
    names = [re.search(r"Alpha|Beta|Gamma|Delta", x).group() for x in _export(tmp_path, b)
             if re.search(r"Alpha|Beta|Gamma|Delta", x)]
    assert names == ["Beta", "Delta", "Gamma", "Alpha"]


def test_fact_tags_clean():
    assert parse_tags("Bug, ui, BUG") == ["bug", "ui"]


def test_fact_find_case():
    b = _board("Fix bug", "Bug report", "Docs")
    assert find(b, "BUG") == [1, 2]


def test_fact_weekdays():
    assert days_left(date(2026, 6, 8), date(2026, 6, 5)) == 1
    assert days_left(date(2026, 6, 15), date(2026, 6, 8)) == 5


def test_fact_title_required():
    b = _board(" Fix ")
    assert b.title(1) == "Fix"
    with pytest.raises(ValueError):
        b.add("   ")
    with pytest.raises(ValueError):
        b.rename(1, "")
    assert b.title(1) == "Fix"


def test_fact_unknown_column():
    b = _board("a")
    b.move(1, "todo")
    with pytest.raises(ValueError):
        b.move(1, "later")
    assert b.column("todo") == [1]


def test_fact_done_locked():
    b = _board("a")
    b.move(1, "done")
    with pytest.raises(ValueError):
        b.move(1, "todo")
    assert b.column("done") == [1]


def test_fact_same_column():
    b = _board("a", "b", "c")
    for i in (1, 2, 3):
        b.move(i, "todo")
    b.move(1, "todo")
    assert b.column("todo") == [1, 2, 3]


def test_fact_count_open():
    b = _board("a", "b", "c")
    b.move(2, "done")
    assert b.count() == 2
