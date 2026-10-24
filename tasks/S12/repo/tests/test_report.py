from report import row_total


def test_row_total():
    assert row_total({"name": "pen", "qty": 2, "price": 3}) == 6
