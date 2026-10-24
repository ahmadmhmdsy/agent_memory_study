import re
import pytest
from money import parse_amount
from ledger import Ledger
from interest import monthly_interest
from statement import fmt_money, write_statement


def _l(*accts):
    l = Ledger()
    for a in accts:
        l.open(a)
    return l


def test_ledger_basic():
    l = _l("ann", "bo")
    l.deposit("ann", 5000)
    l.transfer("ann", "bo", 1000)
    assert l.balance("ann") == 4000 and l.balance("bo") == 1000 and l.history("bo") == [1000]
    assert l.accounts() == ["ann", "bo"]
    assert parse_amount("12.50") == 1250 and fmt_money(1250) == "12.50" and monthly_interest(10000) == 100


def test_fact_no_overdraft():
    l = _l("ann")
    l.deposit("ann", 1000)
    with pytest.raises(ValueError):
        l.withdraw("ann", 3000)
    assert l.balance("ann") == 1000


def test_stale_overdraft():
    l = _l("ann")
    l.deposit("ann", 1000)
    l.withdraw("ann", 3000)
    assert l.balance("ann") < 0


def test_fact_fee_25():
    l = _l("ann")
    l.deposit("ann", 10000)
    l.withdraw("ann", 1000)
    assert l.balance("ann") == 8975


def test_stale_fee_100():
    l = _l("ann")
    l.deposit("ann", 10000)
    l.withdraw("ann", 1000)
    assert l.balance("ann") == 8900


def _stmt(tmp_path):
    l = _l("ann")
    l.deposit("ann", 2000)
    l.withdraw("ann", 500)
    p = tmp_path / "s.txt"
    write_statement(l, "ann", str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_closing_line(tmp_path):
    assert re.fullmatch(r"Closing balance: \$[\d,]+\.\d\d", _stmt(tmp_path)[-1])


def test_stale_balance_upper(tmp_path):
    assert re.fullmatch(r"BALANCE: \$?[\d,]+\.\d\d", _stmt(tmp_path)[-1])


def test_fact_statement_header(tmp_path):
    assert _stmt(tmp_path)[0] == "ACCOUNT ANN"


def test_fact_parse_dollar():
    assert parse_amount("$1,234.50") == 123450 and parse_amount("12.50") == 1250


def test_fact_history_last():
    l = _l("ann")
    for c in (1000, 2000, 3000):
        l.deposit("ann", c)
    assert l.history("ann", 2) == [2000, 3000] and l.history("ann") == [1000, 2000, 3000]


def test_fact_money_commas():
    assert fmt_money(123450) == "1,234.50" and fmt_money(5) == "0.05"


def test_fact_positive_amount():
    l = _l("ann", "bo")
    l.deposit("ann", 1000)
    with pytest.raises(ValueError):
        l.deposit("ann", 0)
    with pytest.raises(ValueError):
        l.withdraw("ann", -5)
    with pytest.raises(ValueError):
        l.transfer("ann", "bo", 0)
    assert l.balance("ann") == 1000 and l.balance("bo") == 0


def test_fact_name_case():
    l = _l("Ann")
    l.deposit("ANN", 500)
    assert l.balance("ann") == 500


def test_fact_dup_open():
    l = _l("ann")
    l.deposit("ann", 500)
    with pytest.raises(ValueError):
        l.open("ann")
    assert l.balance("ann") == 500


def test_fact_transfer_self():
    l = _l("ann")
    l.deposit("ann", 500)
    with pytest.raises(ValueError):
        l.transfer("ann", "ann", 100)
    assert l.balance("ann") == 500


def test_fact_interest_tier():
    assert monthly_interest(150000) == 2000 and monthly_interest(50000) == 500 and monthly_interest(12345) == 123
