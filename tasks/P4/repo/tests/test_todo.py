from todo import TodoList


def test_add_done():
    t = TodoList()
    a = t.add("x")
    t.add("y")
    t.done(a)
    assert [i["title"] for i in t.pending()] == ["y"]
