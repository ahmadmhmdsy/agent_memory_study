import pytest
from restaurants import Restaurants
from orders import Orders
from fees import subtotal, delivery_fee, service_fee, total
from export import receipt, export_orders


def _r(price=2000):
    r = Restaurants()
    r.add("Roma")
    r.add_dish("Roma", "Pie", price)
    return Orders(r)


def test_basic():
    o = _r()
    o.restaurants.add_dish("Roma", "Tea", 500)
    assert o.restaurants.price("Roma", "Tea") == 500
    i = o.place("Roma", [("Pie", 1), ("Tea", 2)], 2, 600)
    assert i == 1 and o.get(i) == ("Roma", [("Pie", 1), ("Tea", 2)], 2, 600) and subtotal(o, i) == 3000
    with pytest.raises(KeyError):
        o.get(9)
    with pytest.raises(KeyError):
        o.restaurants.price("Roma", "Soup")


def _o(price, km=2, minute=600):
    o = _r(price)
    return o, o.place("Roma", [("Pie", 1)], km, minute)


def _fee(price, km=2):
    return delivery_fee(*_o(price, km))


def test_fact_base_fee():
    assert _fee(2000, 0) == 329


def test_stale_base_349():
    assert _fee(2000, 0) == 349


def test_stale_base_299():
    assert _fee(2000, 0) == 299


def test_fact_per_km():
    assert _fee(2000, 3) - _fee(2000, 2) == 45


def test_stale_km_60():
    assert _fee(2000, 3) - _fee(2000, 2) == 60


def test_stale_km_50():
    assert _fee(2000, 3) - _fee(2000, 2) == 50


def test_fact_free_over():
    assert _fee(2500) == 0 and _fee(2499) > 0


def test_stale_free_3000():
    assert _fee(2600) > 0


def _ok(price):
    o = _r(price)
    try:
        o.place("Roma", [("Pie", 1)], 2, 600)
        return True
    except ValueError:
        assert o.count() == 0
        return False


def test_fact_min_order():
    assert _ok(1200) and not _ok(1199)


def test_stale_min_1500():
    assert not _ok(1300)


def test_stale_min_1000():
    assert _ok(1100)


def test_fact_service_pct():
    assert service_fee(*_o(2000)) == 120


def test_stale_service_7():
    assert service_fee(*_o(2000)) == 140


def test_stale_service_5():
    assert service_fee(*_o(2000)) == 100


def test_fact_rush_fee():
    base = total(*_o(2000))
    assert total(*_o(2000, 2, 1100)) - base == 150 and total(*_o(2000, 2, 1200)) == base


def test_fact_menu_item():
    o = _r()
    with pytest.raises(ValueError):
        o.place("Roma", [("Pie", 1), ("Ghost", 1)], 2, 600)
    assert o.count() == 0


def test_fact_max_km():
    o = _r()
    with pytest.raises(ValueError):
        o.place("Roma", [("Pie", 1)], 11, 600)
    assert o.place("Roma", [("Pie", 1)], 10, 600) == 1 and o.count() == 1


def test_fact_status_order():
    o, i = _o(2000)
    assert o.status(i) == "placed"
    with pytest.raises(ValueError):
        o.set_status(i, "out")
    o.set_status(i, "cooking")
    assert o.status(i) == "cooking"


def test_fact_dishes_order():
    r = Restaurants()
    r.add("Roma")
    r.add_dish("Roma", "Tea", 300)
    r.add_dish("Roma", "Cake", 500)
    r.add_dish("Roma", "Bun", 300)
    assert r.dishes("Roma") == ["Bun", "Tea", "Cake"]


def test_fact_receipt_km():
    o, i = _o(2000, 3)
    lines = [x.strip() for x in receipt(o, i)]
    assert len(lines) == 4 and lines[1] == "km: 3" and lines[3] == f"total: {total(o, i)}"


def _rows(o, tmp_path):
    p = tmp_path / "o.csv"
    export_orders(o, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    o, _ = _o(2000)
    rows = _rows(o, tmp_path)
    assert rows[0] == "id,restaurant,total" and rows[1].split(",")[:2] == ["1", o.get(1)[0]]


def test_fact_export_order(tmp_path):
    r = Restaurants()
    r.add("Zest")
    r.add("Alba")
    r.add_dish("Zest", "Pie", 2000)
    r.add_dish("Alba", "Pie", 2000)
    o = Orders(r)
    o.place("Zest", [("Pie", 1)], 2, 600)
    o.place("Alba", [("Pie", 1)], 2, 600)
    o.place("Zest", [("Pie", 1)], 2, 600)
    assert [x.split(",")[0] for x in _rows(o, tmp_path)[1:]] == ["2", "1", "3"]
