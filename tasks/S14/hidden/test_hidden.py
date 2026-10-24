from tickets import TicketBook


def test_add_close():
    b = TicketBook()
    i = b.add("x")
    b.add("y")
    b.close(i)
    assert b.open_titles() == ["y"] and b.count() == 2


def test_fact_ticket_ids():
    b = TicketBook()
    assert b.add("a") == "T0001"
    assert b.add("b") == "T0002"
    assert list(b.tickets) == ["T0001", "T0002"]
