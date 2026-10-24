import pytest
from league import League
from table import standings


def test_basic():
    lg = League()
    lg.record("Ash", "Elm", 2, 1)
    lg.record("Oak", "Ash", 0, 0)
    assert lg.teams() == ["Ash", "Elm", "Oak"] and lg.played("Ash") == 2 and lg.goals_for("Ash") == 2
    assert lg.points("Oak") == 1 and lg.points("Fir") == 0 and standings(lg)[0] == "Ash"


def test_fact_win_points():
    lg = League()
    lg.record("Ash", "Elm", 2, 1)
    assert lg.points("Ash") == 3 and lg.points("Elm") == 0


def test_stale_win_2():
    lg = League()
    lg.record("Ash", "Elm", 2, 1)
    assert lg.points("Ash") == 2


def test_fact_gd_tiebreak():
    lg = League()
    lg.record("Ash", "Bay", 3, 0)
    lg.record("Cob", "Dun", 1, 0)
    assert standings(lg) == ["Ash", "Cob", "Dun", "Bay"]


def test_fact_no_self():
    lg = League()
    with pytest.raises(ValueError):
        lg.record("Ash", "Ash", 1, 0)
    assert lg.teams() == []


def test_fact_goals_nonneg():
    lg = League()
    for hg, ag in ((-1, 0), (0, -2), (1.5, 0)):
        with pytest.raises(ValueError):
            lg.record("Ash", "Elm", hg, ag)
    assert lg.teams() == []


def test_fact_rematch_replace():
    lg = League()
    lg.record("Ash", "Elm", 1, 0)
    lg.record("Ash", "Elm", 1, 1)
    assert lg.played("Ash") == 1 and lg.points("Ash") == 1 and lg.points("Elm") == 1
    lg.record("Elm", "Ash", 0, 0)
    assert lg.played("Ash") == 2
