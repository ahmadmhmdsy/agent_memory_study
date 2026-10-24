import pytest
from account import Account
from statement import statement


def test_basic():
    a = Account()
    a.deposit(1000)
    a.withdraw(300)
    assert a.balance() == 700 and a.history() == [("deposit", 1000), ("withdraw", 300)]
    assert statement(a)[:2] == ["deposit 1000", "withdraw 300"]
    a.add_interest(10)
    assert a.balance() == 770 and a.history()[-1] == ("interest", 70)
    assert a.count("deposit") == 1 and a.count("interest") == 1


def test_fact_overdraft():
    a = Account()
    with pytest.raises(ValueError):
        a.withdraw(2001)
    a.withdraw(2000)
    with pytest.raises(ValueError):
        a.withdraw(1)
    assert a.balance() == -2000 and len(a.history()) == 1


def test_stale_overdraft_5000():
    a = Account()
    a.withdraw(3000)
    assert a.balance() == -3000


def test_fact_balance_line():
    a = Account()
    a.deposit(500)
    a.withdraw(200)
    assert statement(a) == ["deposit 500", "withdraw 200", "balance 300"]


def test_fact_amount_positive():
    a = Account()
    for x in (0, -5, 2.5):
        with pytest.raises(ValueError):
            a.deposit(x)
        with pytest.raises(ValueError):
            a.withdraw(x)
    assert a.balance() == 0 and a.history() == []


def test_fact_deposit_max():
    a = Account()
    a.deposit(1000000)
    with pytest.raises(ValueError):
        a.deposit(1000001)
    assert a.balance() == 1000000 and len(a.history()) == 1


def test_fact_interest_round():
    a = Account()
    a.deposit(1999)
    a.add_interest(5)
    assert a.balance() == 2098
    b = Account()
    b.withdraw(100)
    b.add_interest(5)
    c = Account()
    c.add_interest(5)
    assert b.balance() == -100 and c.balance() == 0
