import datetime as dt
import pytest
from members import Members
from purchases import Purchases
from points import is_gold
from export import card, export_members

D1 = dt.date(2026, 6, 1)


def _p():
    m = Members()
    m.add("Ann")
    return Purchases(m)


def test_basic():
    p = _p()
    i = p.buy("Ann", 250, D1)
    assert i == 1 and p.get(i) == ("Ann", 250, D1) and p.of_member("Ann") == [1]
    assert p.spent("Ann") == 250
    with pytest.raises(KeyError):
        p.get(7)
    with pytest.raises(KeyError):
        p.buy("Bob", 250, D1)


def test_fact_signup_bonus():
    assert _p().members.points("Ann") == 75


def test_stale_signup_100():
    assert _p().members.points("Ann") == 100


def test_stale_signup_50():
    assert _p().members.points("Ann") == 50


def _earn(cents):
    p = _p()
    before = p.members.points("Ann")
    p.buy("Ann", cents, D1)
    return p.members.points("Ann") - before


def test_fact_pts_per():
    assert _earn(599) == 15 and _earn(99) == 0


def test_stale_pts_2():
    assert _earn(599) == 10


def test_stale_pts_1():
    assert _earn(599) == 5


def _cost():
    p = _p()
    p.buy("Ann", 50000, D1)
    before = p.members.points("Ann")
    p.redeem("Ann", D1)
    return before - p.members.points("Ann")


def test_fact_reward_cost():
    assert _cost() == 120


def test_stale_reward_150():
    assert _cost() == 150


def test_stale_reward_100():
    assert _cost() == 100


def _gold(cents):
    p = _p()
    p.buy("Ann", cents, D1)
    return is_gold(p, "Ann")


def test_fact_gold_at():
    assert _gold(120000) and not _gold(119999)


def test_stale_gold_150000():
    assert not _gold(130000)


def test_stale_gold_100000():
    assert _gold(110000)


def test_fact_gold_double():
    p = _p()
    p.buy("Ann", 300000, D1)
    before = p.members.points("Ann")
    p.buy("Ann", 500, D1)
    assert p.members.points("Ann") - before == 2 * _earn(500)


def _per_day():
    p = _p()
    p.buy("Ann", 50000, D1)
    n = 0
    for _ in range(5):
        before = p.members.points("Ann")
        try:
            p.redeem("Ann", D1)
        except ValueError:
            assert p.members.points("Ann") == before
            break
        n += 1
    return n


def test_fact_max_redeem():
    assert _per_day() == 3


def test_stale_redeem_2():
    assert _per_day() == 2


def test_stale_redeem_1():
    assert _per_day() == 1


def test_fact_name_unique():
    m = Members()
    m.add("Ann")
    m.add_points("Ann", 5)
    before = m.points("Ann")
    with pytest.raises(ValueError):
        m.add("Ann")
    assert m.names() == ["Ann"] and m.points("Ann") == before


def test_fact_amount_positive():
    p = _p()
    with pytest.raises(ValueError):
        p.buy("Ann", 0, D1)
    assert p.count() == 0


def test_fact_enough_points():
    p = _p()
    before = p.members.points("Ann")
    with pytest.raises(ValueError):
        p.redeem("Ann", D1)
    assert p.members.points("Ann") == before and p.redeemed("Ann") == 0


def test_fact_names_order():
    m = Members()
    m.add("bob")
    m.add("Cy")
    m.add("Ann")
    assert m.names() == ["Ann", "bob", "Cy"]


def test_fact_card_tier():
    p = _p()
    lines = [x.strip() for x in card(p, "Ann")]
    assert len(lines) == 3 and lines[2] == "tier: basic"
    p.buy("Ann", 300000, D1)
    assert [x.strip() for x in card(p, "Ann")][2] == "tier: gold"


def _rows(p, tmp_path):
    f = tmp_path / "m.csv"
    export_members(p, str(f))
    return [x.rstrip("\r").replace(" ", "") for x in f.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    rows = _rows(_p(), tmp_path)
    assert rows[0] == "name,points" and len(rows) == 2


def test_fact_export_order(tmp_path):
    m = Members()
    m.add("Zoe")
    m.add("Ann")
    m.add("Max")
    p = Purchases(m)
    p.buy("Max", 1000, D1)
    assert [x.split(",")[0] for x in _rows(p, tmp_path)[1:]] == ["Max", "Ann", "Zoe"]
