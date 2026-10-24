import re
import pytest
from parse import parse_line, parse_lines
from stats import by_hour, count_levels, error_rate, slow_requests, summary, top_paths
from report import write_report


def _line(t="12:00:05", level="INFO", method="GET", path="/home", status=200, ms="35ms"):
    return f"2026-06-01 {t} {level} {method} {path} {status} {ms}"


def test_log_basic():
    r = parse_lines([_line(), _line(path="/about", status=404, ms="20ms"), "garbage"])
    assert len(r) == 2 and r[0]["path"] == "/home" and r[0]["status"] == 200 and r[0]["ms"] == 35
    assert count_levels(r) == {"INFO": 2} and top_paths(r, 1)[0][1] == 1
    assert by_hour(r) == {12: 2} and summary(r)["requests"] == 2


def test_fact_slow_300():
    r = parse_lines([_line(ms="400ms"), _line(ms="200ms"), _line(ms="600ms")])
    assert [x["ms"] for x in slow_requests(r)] == [400, 600]


def test_stale_slow_500():
    r = parse_lines([_line(ms="400ms"), _line(ms="200ms"), _line(ms="600ms")])
    assert [x["ms"] for x in slow_requests(r)] == [600]


def _errs():
    return parse_lines([_line(status=s) for s in (200, 404, 500, 200)])


def test_fact_errors_400():
    assert error_rate(_errs()) == 50.0


def test_stale_errors_500():
    assert error_rate(_errs()) == 25.0


def _rep(tmp_path, paths):
    p = tmp_path / "r.txt"
    write_report([_line(path=x) for x in paths], str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_report_line(tmp_path):
    assert "/home: 2 requests" in _rep(tmp_path, ["/home", "/about", "/home"])


def test_stale_report_plain(tmp_path):
    assert "/home 2" in _rep(tmp_path, ["/home", "/about", "/home"])


def test_fact_report_order(tmp_path):
    found = [re.match(r"(/[abc])\b", x) for x in _rep(tmp_path, ["/a", "/b", "/c", "/b", "/c", "/b"])]
    assert [m.group(1) for m in found if m] == ["/b", "/c", "/a"]


def test_fact_report_header(tmp_path):
    assert _rep(tmp_path, ["/home"])[0] == "Log report 2026-06-01"


def test_fact_seconds():
    assert parse_line(_line(ms="1.2s"))["ms"] == 1200 and parse_line(_line(ms="35ms"))["ms"] == 35


def test_fact_query_strip():
    r = parse_lines([_line(path="/a?x=1"), _line(path="/a?y=2"), _line(path="/b")])
    assert top_paths(r, 1) == [("/a", 2)]


def test_fact_hour_fill():
    r = parse_lines([_line(t="09:10:00"), _line(t="12:00:00"), _line(t="12:30:00")])
    assert by_hour(r) == {9: 1, 10: 0, 11: 0, 12: 2}


def test_fact_bad_lines():
    with pytest.raises(ValueError):
        parse_line("nonsense")
    with pytest.raises(ValueError):
        parse_line(_line(status="abc"))
    assert len(parse_lines(["x", _line()])) == 1


def test_fact_method_upper():
    assert parse_line(_line(method="get"))["method"] == "GET"


def test_fact_health_ignored():
    r = parse_lines([_line(path="/health", status=500), _line(), _line(path="/health")])
    assert error_rate(r) == 0.0 and top_paths(r, 5) == [("/home", 1)]


def test_fact_error_round():
    assert error_rate(parse_lines([_line(status=s) for s in (404, 200, 200)])) == 33.3
