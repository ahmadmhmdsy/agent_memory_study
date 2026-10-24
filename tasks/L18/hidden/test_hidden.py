import re
from datetime import date, timedelta
import pytest
from urls import domain_of, normalize
from store import Shortener
from report import write_report

D0 = date(2026, 6, 1)


def test_short_basic():
    s = Shortener()
    c = s.shorten("example.com/a", D0)
    assert s.expand(c, D0) == "https://example.com/a" and s.stats(c) == 1
    assert s.expand("nope", D0) is None and s.count(D0) == 1
    assert s.by_domain() == {"example.com": 1} and domain_of("https://example.com/a") == "example.com"
    s.delete(c)
    assert s.expand(c, D0) is None and s.count(D0) == 0


def test_fact_code_7():
    s = Shortener()
    codes = [s.shorten(f"https://e.com/{i}", D0) for i in range(30)]
    assert all(len(c) == 7 for c in codes) and len(set(codes)) == 30


def test_stale_code_6():
    s = Shortener()
    assert all(len(s.shorten(f"https://e.com/{i}", D0)) == 6 for i in range(30))


def test_fact_expire_90():
    s = Shortener()
    c = s.shorten("https://e.com/a", D0)
    assert s.expand(c, D0 + timedelta(days=60)) == "https://e.com/a"
    assert s.expand(c, D0 + timedelta(days=90)) is None


def test_stale_expire_30():
    s = Shortener()
    c = s.shorten("https://e.com/a", D0)
    assert s.expand(c, D0 + timedelta(days=60)) is None


def _rep(tmp_path, s):
    p = tmp_path / "r.txt"
    write_report(s, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def _docs():
    s = Shortener()
    s.shorten("https://example.com/docs", D0, alias="docs")
    for _ in range(3):
        s.expand("docs", D0)
    return s


def test_fact_report_line(tmp_path):
    assert "docs | 3 clicks | https://example.com/docs" in _rep(tmp_path, _docs())


def test_stale_report_plain(tmp_path):
    assert "docs https://example.com/docs 3" in _rep(tmp_path, _docs())


def _three():
    s = Shortener()
    for a, n in (("aaa", 1), ("bbb", 3), ("ccc", 2)):
        s.shorten(f"https://x.com/{n}", D0, alias=a)
        for _ in range(n):
            s.expand(a, D0)
    return s


def test_fact_report_order(tmp_path):
    found = [re.search(r"\b(aaa|bbb|ccc)\b", x) for x in _rep(tmp_path, _three())]
    assert [m.group(1) for m in found if m] == ["bbb", "ccc", "aaa"]


def test_fact_report_header(tmp_path):
    assert _rep(tmp_path, _three())[0] == "Links: 3"


def test_fact_normalize_host():
    assert normalize("https://Example.COM/a/") == "https://example.com/a"
    assert normalize("Example.com/Path/") == "https://example.com/Path"


def test_fact_stats_day():
    s = Shortener()
    c = s.shorten("https://e.com/a", D0)
    for d in (0, 1, 1):
        s.expand(c, D0 + timedelta(days=d))
    assert s.stats(c, D0 + timedelta(days=1)) == 2 and s.stats(c) == 3


def test_fact_strip_www():
    assert domain_of("https://www.example.com/a") == "example.com"
    assert domain_of("http://shop.example.com") == "shop.example.com"


def test_fact_scheme_check():
    with pytest.raises(ValueError):
        normalize("ftp://x.com/a")
    with pytest.raises(ValueError):
        Shortener().shorten("ftp://x.com/a", D0)
    assert normalize("http://x.com") == "http://x.com"


def test_fact_same_url():
    s = Shortener()
    a = s.shorten("https://e.com/a", D0)
    b = s.shorten("https://e.com/a", D0)
    assert a == b and s.count(D0) == 1


def test_fact_alias_rules():
    s = Shortener()
    s.shorten("https://e.com/1", D0, alias="docs")
    for bad in ("docs", "ab", "a!b"):
        with pytest.raises(ValueError):
            s.shorten("https://e.com/2", D0, alias=bad)
    assert s.expand("docs", D0) == "https://e.com/1"


def test_fact_no_confusable():
    s = Shortener()
    codes = [s.shorten(f"https://e.com/{i}", D0) for i in range(200)]
    assert not any(ch in "0O1lI" for c in codes for ch in c)
