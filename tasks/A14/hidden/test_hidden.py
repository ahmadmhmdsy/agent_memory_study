import datetime as dt
import pytest
from customers import Customers
from jobs import Jobs
from pricing import price
from export import ticket, export_jobs

D1, D2 = dt.date(2026, 5, 1), dt.date(2026, 5, 4)


def _j():
    c = Customers()
    c.add("Ann")
    return Jobs(c)


def test_basic():
    j = _j()
    assert j.customers.has("Ann") and not j.customers.has("Bob")
    i = j.add("Ann", 20, "A4", D1, D2)
    assert i == 1 and j.get(i) == ("Ann", 20, "A4", D1, D2) and j.of_customer("Ann") == [1]
    assert not j.is_color(i) and not j.is_bound(i) and not j.is_rush(i)
    with pytest.raises(KeyError):
        j.get(3)
    with pytest.raises(KeyError):
        j.add("Bob", 5, "A4", D1, D2)


def _job(pages, size="A4", color=False, bound=False, rush=False):
    j = _j()
    i = j.add("Ann", pages, size, D1, D2)
    if color:
        j.set_color(i)
    if bound:
        j.bind(i)
    if rush:
        j.set_rush(i)
    return price(j, i)


def test_fact_bw_page():
    assert _job(1) == 12


def test_stale_bw_8():
    assert _job(1) == 8


def test_stale_bw_10():
    assert _job(1) == 10


def test_fact_color_page():
    assert _job(1, color=True) == 45


def test_stale_color_40():
    assert _job(1, color=True) == 40


def test_stale_color_50():
    assert _job(1, color=True) == 50


def test_fact_a3_double():
    assert _job(3, "A3") == 2 * _job(3) and _job(3, "A3", True) == 2 * _job(3, color=True)


def test_fact_bulk_pages():
    one = _job(1)
    assert _job(249) == 249 * one and _job(250) < 250 * one


def test_stale_bulk_1000():
    assert _job(999) == 999 * _job(1)


def test_stale_bulk_500():
    assert _job(499) == 499 * _job(1)


def test_fact_bulk_pct():
    assert _job(400) == round(400 * _job(1) * 90 / 100)


def test_fact_binding_fee():
    assert _job(10, bound=True) - _job(10) == 400


def test_stale_binding_500():
    assert _job(10, bound=True) - _job(10) == 500


def test_stale_binding_300():
    assert _job(10, bound=True) - _job(10) == 300


def test_fact_rush_pct():
    x = _job(10)
    assert _job(10, rush=True) - x == round(x * 25 / 100)


def test_stale_rush_50():
    x = _job(10)
    assert _job(10, rush=True) - x == round(x * 50 / 100)


def test_fact_paper_size():
    j = _j()
    with pytest.raises(ValueError):
        j.add("Ann", 5, "A5", D1, D2)
    assert j.of_customer("Ann") == []


def test_fact_pages_positive():
    j = _j()
    with pytest.raises(ValueError):
        j.add("Ann", 0, "A4", D1, D2)
    assert j.of_customer("Ann") == []


def test_fact_due_after():
    j = _j()
    with pytest.raises(ValueError):
        j.add("Ann", 5, "A4", D2, D1)
    assert j.add("Ann", 5, "A4", D1, D1) == 1 and j.of_customer("Ann") == [1]


def test_fact_names_order():
    c = Customers()
    c.add("Zoe")
    c.add("Ann")
    c.add("Max")
    assert c.names() == ["Ann", "Max", "Zoe"]


def test_fact_ticket_due():
    j = _j()
    i = j.add("Ann", 20, "A4", D1, D2)
    lines = [x.strip() for x in ticket(j, i)]
    assert len(lines) == 3 and lines[2] == f"due: {D2.isoformat()}"


def _rows(j, tmp_path):
    p = tmp_path / "j.csv"
    export_jobs(j, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    j = _j()
    j.add("Ann", 20, "A4", D1, D2)
    rows = _rows(j, tmp_path)
    assert rows[0] == "id,customer,pages,price" and rows[1].split(",")[1:3] == ["Ann", "20"]


def test_fact_export_order(tmp_path):
    j = _j()
    j.add("Ann", 5, "A4", D1, D2)
    j.add("Ann", 5, "A4", D1, D1)
    j.add("Ann", 5, "A4", D1, D2)
    assert [x.split(",")[0] for x in _rows(j, tmp_path)[1:]] == ["2", "1", "3"]
