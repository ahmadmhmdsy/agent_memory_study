from text import clean_title, slug
from timeutil import parse_ts


class Calendar:
    def __init__(self):
        self.items = []

    def add(self, title, start, end):
        title = clean_title(title)
        if not title:
            raise ValueError("empty title")
        if len(title) > 40:
            raise ValueError("title too long")
        s, e = parse_ts(start), parse_ts(end)
        if e < s:
            raise ValueError("end before start")
        if (e - s).total_seconds() > 24 * 3600:
            raise ValueError("event longer than 24 hours")
        for x in self.items:
            if s < parse_ts(x["end"]) and parse_ts(x["start"]) < e:
                raise ValueError("overlaps an existing event")
        eid = f"EVT-{len(self.items) + 1:05d}"
        self.items.append({"id": eid, "title": title, "start": start, "end": end})
        return eid

    def events(self):
        items = sorted(self.items, key=lambda e: (parse_ts(e["start"]), e["title"]))
        return [dict(e, slug=slug(e["title"])) for e in items]

    def duration(self, event_id):
        e = next(e for e in self.items if e["id"] == event_id)
        return int((parse_ts(e["end"]) - parse_ts(e["start"])).total_seconds() // 60)
