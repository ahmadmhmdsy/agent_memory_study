from report import row_total, totals, export


def test_totals():
    rows = [{"name": "pen", "qty": 2, "price": 3}, {"name": "pen", "qty": 1, "price": 3},
            {"name": "cup", "qty": 1, "price": 5}]
    assert totals(rows) == {"pen": 9, "cup": 5}


def test_fact_semicolon_csv(tmp_path):
    p = tmp_path / "r.csv"
    export([{"name": "pen", "qty": 2, "price": 3}, {"name": "cup", "qty": 1, "price": 5}], str(p))
    lines = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert lines == ["name;qty;price", "pen;2;3", "cup;1;5"]
