import datetime as dt
import re
import pytest
from catalog import Catalog, normalize_isbn, search
from loans import Loans, member_id
from fines import fine
from export import export_loans

D = dt.date
A, B, C, E = "9780000000001", "9780000000002", "9780000000003", "9780000000004"


def test_loans_basic():
    l = Loans()
    l.checkout(A, "ann", D(2026, 1, 1))
    assert l.holder(A) == "ann" and l.holder(B) is None
    l.return_book(A, D(2026, 1, 2))
    assert l.holder(A) is None
    assert fine(D(2026, 1, 10), D(2026, 1, 10)) == 0 and fine(D(2026, 1, 10), D(2026, 1, 5)) == 0


def _due():
    l = Loans()
    l.checkout(A, "ann", D(2026, 1, 1))
    return l.due(A)


def test_fact_loan_days():
    assert _due() == D(2026, 1, 22)


def test_stale_loan_14():
    assert _due() == D(2026, 1, 15)


def test_fact_fine_rate():
    assert fine(D(2026, 1, 10), D(2026, 1, 13)) == 150


def test_stale_fine_25():
    assert fine(D(2026, 1, 10), D(2026, 1, 13)) == 75


def _rows(tmp_path):
    l = Loans()
    l.checkout(B, "bob", D(2026, 3, 1))
    l.checkout(A, "ann", D(2026, 1, 1))
    p = tmp_path / "l.csv"
    export_loans(l, str(p))
    return [x.rstrip("\r") for x in p.read_text().splitlines() if x.strip()]


def test_fact_date_iso(tmp_path):
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", re.split(r"[,;\t]", _rows(tmp_path)[-1])[-1].strip())


def test_stale_date_dmy(tmp_path):
    assert re.fullmatch(r"\d{2}/\d{2}/\d{4}", re.split(r"[,;\t]", _rows(tmp_path)[-1])[-1].strip())


def test_fact_export_header(tmp_path):
    rows = _rows(tmp_path)
    assert rows[0].replace(" ", "") == "isbn,member,due" and rows[1].split(",")[:2] == [A, "ann"]


def test_fact_isbn_hyphens():
    assert normalize_isbn("978-0-306-40615-7") == "9780306406157"
    assert normalize_isbn("978 0 306 40615 7") == "9780306406157"
    with pytest.raises(ValueError):
        normalize_isbn("12-34")


def test_fact_search_sorted():
    c = Catalog()
    c.add(C, "Big apple")
    c.add(A, "Apple pie")
    c.add(B, "Apple cake")
    c.add(E, "Pears")
    assert search(c, "APPLE") == [B, A, C]


def test_fact_member_ascii():
    assert member_id("José O'Neil") == "jose-oneil" and member_id("Ada Lovelace") == "ada-lovelace"


def test_fact_member_case():
    l = Loans()
    l.checkout(A, "Ann", D(2026, 1, 1))
    assert l.holder(A) == "ann" and l.books_of("ANN") == [A]


def test_fact_max_loans():
    l = Loans()
    for i in (A, B, C):
        l.checkout(i, "ann", D(2026, 1, 1))
    with pytest.raises(ValueError):
        l.checkout(E, "ann", D(2026, 1, 1))
    assert l.holder(E) is None and l.books_of("ann") == [A, B, C]


def test_fact_double_loan():
    l = Loans()
    l.checkout(A, "ann", D(2026, 1, 1))
    with pytest.raises(ValueError):
        l.checkout(A, "bob", D(2026, 1, 2))
    assert l.holder(A) == "ann"


def test_fact_return_unknown():
    l = Loans()
    l.checkout(A, "ann", D(2026, 1, 1))
    l.return_book(B, D(2026, 1, 2))
    assert l.holder(A) == "ann"


def test_fact_fine_cap():
    assert fine(D(2026, 1, 1), D(2026, 6, 1)) == 1000
