from cache import Cache


def test_basic_and_stats():
    c = Cache()
    c.put("a", 1)
    assert c.get("a") == 1 and c.get("b", 0) == 0
    assert c.stats() == {"hits": 1, "misses": 1}


def test_limit_keeps_size():
    c = Cache(max_items=2)
    for k in "abcd":
        c.put(k, k)
    assert sum(c.get(k) is not None for k in "abcd") == 2


def test_fact_lfu_eviction():
    c = Cache(max_items=2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")
    c.get("a")
    c.get("b")
    c.put("c", 3)  # b has fewer reads than a, though a was read less recently
    assert c.get("a") == 1 and c.get("c") == 3 and c.get("b") is None
    # tie on reads: the key first added earliest goes, even after an update
    c = Cache(max_items=2)
    c.put("x", 1)
    c.put("y", 2)
    c.put("x", 9)  # an update, not a new key: nothing evicted
    c.put("z", 3)
    assert c.get("x") is None and c.get("y") == 2 and c.get("z") == 3
