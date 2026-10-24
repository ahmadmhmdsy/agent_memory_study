class Cache:
    def __init__(self, max_items=None):
        self.max_items = max_items
        self.data = {}
        self.reads = {}
        self.hits = 0
        self.misses = 0

    def put(self, key, value):
        if key not in self.data and self.max_items is not None and len(self.data) >= self.max_items:
            victim = min(self.data, key=lambda k: self.reads[k])  # dict order = insertion order
            del self.data[victim]
            del self.reads[victim]
        if key not in self.data:
            self.reads[key] = 0
        self.data[key] = value

    def get(self, key, default=None):
        if key in self.data:
            self.hits += 1
            self.reads[key] += 1
            return self.data[key]
        self.misses += 1
        return default

    def stats(self):
        return {"hits": self.hits, "misses": self.misses}
