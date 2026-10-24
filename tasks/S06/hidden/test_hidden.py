from export import make_task, pending, write_csv


def test_pending():
    ts = [make_task("a", True), make_task("b")]
    assert [t["title"] for t in pending(ts)] == ["b"]


def test_fact_csv_booleans(tmp_path):
    p = tmp_path / "t.csv"
    write_csv([make_task("a", True), make_task("b")], str(p))
    lines = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert lines == ["title,done", "a,Y", "b,N"]
