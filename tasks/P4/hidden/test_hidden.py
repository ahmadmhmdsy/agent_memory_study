import json
import os

import pytest

from todo import TodoList


def test_remove_rename():
    t = TodoList()
    a = t.add("x")
    t.rename(a, "z")
    assert t.items[0]["title"] == "z"
    t.remove(a)
    assert t.items == []
    with pytest.raises(KeyError):
        t.remove(99)


def test_priority():
    t = TodoList()
    t.add("l", priority="low")
    t.add("h", priority="high")
    t.add("n")
    assert [i["title"] for i in t.by_priority()] == ["h", "n", "l"]
    with pytest.raises(ValueError):
        t.add("bad", priority="urgent")


def test_round_trip(tmp_path):
    t = TodoList()
    a = t.add("a", priority="high")
    t.add("b")
    t.done(a)
    t.save(str(tmp_path))
    u = TodoList.load(str(tmp_path))
    assert [(i["title"], i["done"]) for i in u.items] == [("a", True), ("b", False)]
    new_id = u.add("c")
    assert new_id not in (1, 2)


def test_fact_jsonl_file(tmp_path):
    t = TodoList()
    t.add("a")
    t.add("b")
    t.save(str(tmp_path))
    path = os.path.join(str(tmp_path), "todos.jsonl")
    assert os.path.exists(path)
    lines = [l for l in open(path, encoding="utf8").read().splitlines() if l.strip()]
    assert len(lines) == 2
    rows = [json.loads(l) for l in lines]
    assert all(isinstance(r, dict) for r in rows)
    assert [r["title"] for r in rows] == ["a", "b"]
