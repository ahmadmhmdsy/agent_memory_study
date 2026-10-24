import pytest
from bank import Account


def test_basics():
    a = Account()
    a.deposit(100)
    a.withdraw(30)
    with pytest.raises(ValueError):
        a.withdraw(1000)
    assert a.balance == 70 and a.transaction_count() == 2 and a.largest_deposit() == 100


def test_fact_statement():
    a = Account()
    a.deposit(100)
    a.withdraw(30)
    a.deposit(5)
    assert a.statement() == ["+100", "-30", "+5"]
