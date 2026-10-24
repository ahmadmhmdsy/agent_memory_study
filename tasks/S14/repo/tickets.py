"""Ticket tracker. tickets maps a ticket id to {"title": str, "open": bool}."""


class TicketBook:
    def __init__(self):
        self.tickets = {}
