from tickets import TicketBook


def test_empty():
    assert TicketBook().count() == 0
