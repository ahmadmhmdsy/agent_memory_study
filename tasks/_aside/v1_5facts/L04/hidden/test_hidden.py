import json
import pytest
from todo import TodoList
from storage import save, load
from util import parse_tags


def test_todo_basic(tmp_path):
    t = TodoList()
    assert t.add("pay rent", 1, "2026-03-01") == 1
    assert t.add("call bob", 2) == 2
    p = tmp_path / "t.json"
    save(t, str(p))
    back = load(str(p))
    assert [x["title"] for x in back.tasks()] == ["pay rent", "call bob"]
    assert back.tasks()[0]["due"] == "2026-03-01" and back.tasks()[1]["due"] is None


def test_fact_sorted():
    t = TodoList()
    t.add("a", 2)
    t.add("b", 1)
    t.add("c", 2)
    t.add("d", 1)
    assert [x["title"] for x in t.tasks()] == ["b", "d", "a", "c"]


def _saved(tmp_path):
    t = TodoList()
    t.add("a", 1)
    p = tmp_path / "t.json"
    save(t, str(p))
    return json.loads(p.read_text())


def test_fact_save_format(tmp_path):
    d = _saved(tmp_path)
    assert d.get("version") == 2 and isinstance(d.get("tasks"), list) and len(d["tasks"]) == 1


def test_stale_items_key(tmp_path):
    assert "items" in _saved(tmp_path)


def test_fact_due():
    t = TodoList()
    for bad in ("2026-02-30", "2026/01/01", "tomorrow"):
        with pytest.raises(ValueError):
            t.add("x", 1, bad)
    t.add("x", 1, "2026-01-31")


def test_fact_title_len():
    t = TodoList()
    with pytest.raises(ValueError):
        t.add("x" * 61, 1)
    t.add("x" * 60, 1)
    t.add("  " + "y" * 60 + "  ", 1)


def test_fact_tags():
    assert parse_tags("Home, work ,home,,WORK, x") == ["home", "work", "x"]
