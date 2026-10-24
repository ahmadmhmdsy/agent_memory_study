class TicketBook:
    def __init__(self):
        self.tickets = {}

    def count(self):
        return len(self.tickets)

    def close(self, ticket_id):
        self.tickets[ticket_id]["open"] = False

    def open_titles(self):
        return [t["title"] for t in self.tickets.values() if t["open"]]

    def add(self, title):
        tid = f"T{len(self.tickets) + 1:04d}"
        self.tickets[tid] = {"title": title, "open": True}
        return tid
