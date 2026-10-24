import csv
import pytest
from phones import normalize_phone
from names import initials
from book import AddressBook
from export import write_csv


def _b():
    b = AddressBook()
    b.add("Cy Abbot", phone="+44 20 7946 0000")
    b.add("Ann Zed", email="ann@zed.org")
    b.add("Bo Lee", phone="+31 6 1111 2222", email="bo@lee.nl")
    return b


def test_book_basic():
    b = _b()
    g = b.get("Bo Lee")
    assert g["name"] == "Bo Lee" and g["phone"] == "+31611112222" and g["email"] == "bo@lee.nl"
    assert b.get("Ann Zed")["phone"] is None
    b.update("Bo Lee", email="bo@new.nl")
    assert b.get("Bo Lee")["email"] == "bo@new.nl" and b.get("Bo Lee")["phone"] == "+31611112222"
    assert b.count() == 3 and b.search("lee") == ["Bo Lee"] and initials("Ann Zed") == "AZ"
    b.remove("Cy Abbot")
    assert b.count() == 2 and normalize_phone("+31 6 12") == "+31612"


def test_fact_first_name():
    assert _b().names() == ["Ann Zed", "Bo Lee", "Cy Abbot"]


def test_stale_last_name():
    assert _b().names() == ["Cy Abbot", "Bo Lee", "Ann Zed"]


def test_fact_country_49():
    assert normalize_phone("0612345678") == "+49612345678"


def test_stale_country_31():
    assert normalize_phone("0612345678") == "+31612345678"


def _csv(tmp_path):
    p = tmp_path / "c.csv"
    write_csv(_b(), str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_csv_header(tmp_path):
    assert _csv(tmp_path)[0] == "name,email,phone"


def test_stale_csv_header(tmp_path):
    assert _csv(tmp_path)[0] == "name,phone,email"


def test_fact_export_empty(tmp_path):
    rows = [r for r in csv.DictReader(_csv(tmp_path)) if not r["name"].startswith("#")]
    ann = next(r for r in rows if r["name"] == "Ann Zed")
    assert ann["phone"] == "" and ann["email"] == "ann@zed.org"


def test_fact_export_count(tmp_path):
    assert _csv(tmp_path)[-1] == "# 3 contacts"


def test_fact_phone_marks():
    assert normalize_phone("+31 (6) 12-34.56") == "+316123456"


def test_fact_search_email():
    b = _b()
    assert b.search("zed.org") == ["Ann Zed"] and b.search("abbot") == ["Cy Abbot"]


def test_fact_initials_hyphen():
    assert initials("Mary-Jane Lee") == "MJL" and initials("Ann Zed") == "AZ"


def test_fact_email_valid():
    b = AddressBook()
    for bad in ("ann", "ann@@x.org", "@x.org", "ann@xorg"):
        with pytest.raises(ValueError):
            b.add("Ann Zed", email=bad)
    assert b.count() == 0
    b.add("Ann Zed", email="ann@zed.org")
    with pytest.raises(ValueError):
        b.update("Ann Zed", email="nope")
    assert b.get("Ann Zed")["email"] == "ann@zed.org"


def test_fact_name_title():
    b = AddressBook()
    b.add("ann van zed", email="a@b.nl")
    assert b.names() == ["Ann Van Zed"]


def test_fact_dup_name():
    b = AddressBook()
    b.add("Ann Zed", email="ann@zed.org")
    with pytest.raises(ValueError):
        b.add("ann zed", phone="+3161")
    assert b.count() == 1


def test_fact_contact_needs():
    b = AddressBook()
    with pytest.raises(ValueError):
        b.add("Ann Zed")
    assert b.count() == 0
