from export import make_task


def test_make_task():
    assert make_task("a") == {"title": "a", "done": False}
