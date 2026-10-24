import pytest
from library import Library
from fees import late_fee


def _lib():
    lib = Library()
    for i in "1234":
        lib.add_book("isbn" + i, "Book " + i)
    return lib


def test_basic():
    lib = _lib()
    lib.lend("isbn1", "ann", 0)
    lib.lend("isbn2", "bob", 3)
    assert lib.is_out("isbn1") and not lib.is_out("isbn3")
    assert lib.held("ann") == ["isbn1"] and lib.held("zed") == []
    lib.give_back("isbn1")
    assert not lib.is_out("isbn1") and lib.titles() == ["Book 1", "Book 3", "Book 4"]


def test_fact_loan_days():
    lib = _lib()
    lib.lend("isbn1", "ann", 5)
    assert lib.due("isbn1") == 26 and late_fee(lib, "isbn1", 26) == 0 and late_fee(lib, "isbn1", 30) == 100


def test_stale_loan_14():
    lib = _lib()
    lib.lend("isbn1", "ann", 5)
    assert lib.due("isbn1") == 19


def test_fact_fee_cap():
    lib = _lib()
    lib.lend("isbn1", "ann", 0)
    assert late_fee(lib, "isbn1", 30) == 225 and late_fee(lib, "isbn1", 100) == 500


def test_fact_no_double_lend():
    lib = _lib()
    lib.lend("isbn1", "ann", 0)
    with pytest.raises(ValueError):
        lib.lend("isbn1", "bob", 1)
    assert lib.held("ann") == ["isbn1"] and lib.held("bob") == []


def test_fact_member_limit():
    lib = _lib()
    for i in "123":
        lib.lend("isbn" + i, "ann", 0)
    with pytest.raises(ValueError):
        lib.lend("isbn4", "ann", 0)
    assert not lib.is_out("isbn4") and len(lib.held("ann")) == 3


def test_fact_return_unknown():
    lib = _lib()
    for isbn in ("isbn9", "isbn2"):
        with pytest.raises(KeyError):
            lib.give_back(isbn)
