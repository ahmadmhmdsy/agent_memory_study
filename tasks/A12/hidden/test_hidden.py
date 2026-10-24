import pytest
from players import Players
from games import Games
from standings import points, is_provisional, entry_fee
from export import result_text, export_table


def _g(**ratings):
    p = Players()
    for n, r in (ratings or {"Ann": 1500, "Bob": 1500}).items():
        p.add(n, r)
    return Games(p)


def test_basic():
    g = _g()
    i = g.record("Ann", "Bob", "1/2")
    assert i == 1 and g.get(i) == ("Ann", "Bob", "1/2") and g.of_player("Bob") == [1]
    with pytest.raises(KeyError):
        g.get(4)
    with pytest.raises(KeyError):
        g.record("Ann", "Cy", "1-0")


def _pts(result):
    g = _g()
    g.record("Ann", "Bob", result)
    return points(g, "Ann"), points(g, "Bob")


def test_fact_win_pts():
    assert _pts("1-0") == (3, 0) and _pts("0-1") == (0, 3)


def test_stale_win_2():
    assert _pts("1-0") == (2, 0)


def test_fact_draw_pts():
    g = _g()
    g.record("Ann", "Bob", "1/2")
    assert _pts("1/2") == (1, 1) and g.players.rating("Ann") == g.players.rating("Bob") == 1500


def _gain():
    g = _g()
    g.record("Ann", "Bob", "1-0")
    return g.players.rating("Ann") - 1500


def _lose(r):
    g = _g(Ann=1500, Bob=r)
    g.record("Ann", "Bob", "1-0")
    return g.players.rating("Bob")


def test_fact_k_factor():
    assert _gain() == 24 and _lose(1500) == 1476


def test_stale_k_20():
    assert _gain() == 20


def test_stale_k_32():
    assert _gain() == 32


def test_fact_rating_floor():
    k = _gain()
    assert _lose(310) == 300 and _lose(330) == 330 - k


def test_stale_floor_400():
    assert _lose(410) == 400


def test_stale_floor_100():
    assert _lose(310) == 310 - _gain()


def _prov(n):
    g = _g(Ann=1500, **{f"P{k}": 1500 for k in range(10)})
    for k in range(n):
        g.record("Ann", f"P{k}", "1/2")
    return is_provisional(g, "Ann")


def test_fact_provisional():
    assert _prov(7) and not _prov(8)


def test_stale_prov_10():
    assert _prov(9)


def test_stale_prov_5():
    assert not _prov(5)


def test_fact_entry_fee():
    assert entry_fee() == 1800


def test_stale_fee_2000():
    assert entry_fee() == 2000


def test_stale_fee_1500():
    assert entry_fee() == 1500


def test_fact_result_valid():
    g = _g()
    with pytest.raises(ValueError):
        g.record("Ann", "Bob", "2-0")
    assert g.of_player("Ann") == []


def test_fact_not_self():
    g = _g()
    with pytest.raises(ValueError):
        g.record("Ann", "Ann", "1-0")
    assert g.of_player("Ann") == []


def test_fact_pair_limit():
    g = _g()
    g.record("Ann", "Bob", "1/2")
    g.record("Bob", "Ann", "1/2")
    with pytest.raises(ValueError):
        g.record("Ann", "Bob", "1/2")
    assert g.of_player("Ann") == [1, 2]


def test_fact_names_order():
    p = Players()
    p.add("Zoe", 1500)
    p.add("Ann", 1500)
    p.add("Max", 1600)
    assert p.names() == ["Max", "Ann", "Zoe"]


def test_fact_score_line():
    g = _g()
    assert result_text(g, g.record("Ann", "Bob", "1/2")).strip() == "Ann - Bob: draw"


def _rows(g, tmp_path):
    p = tmp_path / "t.csv"
    export_table(g, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    rows = _rows(_g(), tmp_path)
    assert rows[0] == "name,points,rating" and len(rows) == 3


def test_fact_export_order(tmp_path):
    g = _g(Zoe=1500, Ann=1500, Max=1500)
    g.record("Zoe", "Max", "0-1")
    assert [x.split(",")[0] for x in _rows(g, tmp_path)[1:]] == ["Max", "Ann", "Zoe"]
