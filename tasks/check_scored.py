"""Checks each scored task: (1) the reference passes the visible and hidden tests; (2) a default
version, the reference with the fact-bearing code replaced by what a model would write without the
fact, passes the plain hidden tests and fails every test_fact test."""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))

# Appended to the reference module: the "no memory" choice for the fact-bearing code.
DEFAULTS = {
    "S01": "def next_business_day(d):\n    d = d + timedelta(days=1)\n    while d.weekday() >= 5:\n        d += timedelta(days=1)\n    return d\n",
    "S02": "def unique_scores(scores):\n    return sorted(set(scores))\n",
    "S03": "def parse_date_iso(s):\n    return date.fromisoformat(s)\n",
    "S04": "class InventoryError(ValueError):\n    pass\n"
           "def _rm(self, name, qty):\n    if qty > self.quantity(name):\n        raise InventoryError(name)\n    self.stock[name] -= qty\n"
           "Inventory.remove_stock = _rm\n",
    "S05": "def discount_rate(t):\n    return 10 if t >= 200 else 5 if t >= 100 else 0\n"
           "def growth(old, new):\n    return round((new - old) / old * 100, 2)\n",
    "S06": "def write_csv(tasks, path):\n    with open(path, 'w') as f:\n        f.write('title,done\\n')\n"
           "        for t in tasks:\n            f.write(f\"{t['title']},{t['done']}\\n\")\n",
    "S07": "_norm = lambda name: name\n",
    "S08": "def average(readings):\n    return sum(readings) / len(readings)\n",
    "S09": "def _put(self, key, value):\n"
           "    if key not in self.data and self.max_items is not None and len(self.data) >= self.max_items:\n"
           "        victim = next(iter(self.data)); del self.data[victim]; del self.reads[victim]\n"
           "    if key not in self.data:\n        self.reads[key] = 0\n    self.data[key] = value\n"
           "Cache.put = _put\n",
    "S10": "def page(items, number, size):\n    return list(items[(number - 1) * size:number * size]) if number >= 1 else []\n",
    "S11": "def slugify(title):\n    return '-'.join(clean(title).split())\n",
    "S12": "def export(rows, path):\n    with open(path, 'w', newline='') as f:\n        w = csv.writer(f)\n"
           "        w.writerow(['name', 'qty', 'price'])\n        for r in rows:\n            w.writerow([r['name'], r['qty'], r['price']])\n",
    "S13": "def _log(self, msg, now):\n    self.entries.append(f'{now.astimezone(timezone.utc).isoformat()} {msg}')\nLogger.log = _log\n",
    "S14": "def _add(self, title):\n    tid = len(self.tickets) + 1\n    self.tickets[tid] = {'title': title, 'open': True}\n    return tid\nTicketBook.add = _add\n",
    "S15": "def get(cfg, key, default=None):\n    return cfg.get(key, default)\n",
    "S16": "def average(scores):\n    return sum(scores) / len(scores)\n",
    "S17": "def _peek(self):\n    return self.items[-1]\nStack.peek = _peek\n",
    "S18": "def truncate(s, n):\n    return s if len(s) <= n else s[:n] + '...'\n",
    "S19": "def letter(score):\n    return 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F'\n",
    "S20": "def _low(self, threshold=10):\n    return [n for n, q in self.stock.items() if q <= threshold]\nStore.low_stock = _low\n",
    "S21": "def to_seconds(s):\n    nums = [int(x) for x in s.split(':')]\n    while len(nums) < 3:\n        nums.append(0)\n"
           "    return nums[0] * 3600 + nums[1] * 60 + nums[2]\n",
    "S22": "from urllib.parse import parse_qs\ndef query_params(url):\n    return parse_qs(urlsplit(url).query)\n",
    "S23": "def _st(self):\n    return [('Deposit' if m > 0 else 'Withdrawal') + f': {abs(m)}' for m in self.moves]\nAccount.statement = _st\n",
    "S24": "def rare_words(text, max_count=1):\n    return [w for w, c in counts(text).items() if c <= max_count]\n",
}


def pytest(cwd, target, env):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rA", target],
                       cwd=cwd, env=env, capture_output=True, text=True)
    res = {name: status for status, name in re.findall(r"^(PASSED|FAILED|ERROR) \S+::(\w+)", p.stdout, re.M)}
    return p.returncode, res, p.stdout


def check(tid):
    import json
    base = os.path.join(ROOT, tid)
    module = json.load(open(os.path.join(base, "sessions.json"), encoding="utf8"))["module"]
    ref = open(os.path.join(base, "ref.py"), encoding="utf8").read()
    problems = []
    for variant, src in (("ref", ref), ("default", ref + "\n\n" + DEFAULTS[tid])):
        with tempfile.TemporaryDirectory() as tmp:
            repo = os.path.join(tmp, "repo")
            shutil.copytree(os.path.join(base, "repo"), repo)
            with open(os.path.join(repo, module), "w", encoding="utf8") as f:
                f.write(src)
            env = {**os.environ, "PYTHONPATH": repo, "PYTHONIOENCODING": "utf8"}
            hcode, hidden, out = pytest(repo, os.path.join(base, "hidden"), env)
            facts = {n: s for n, s in hidden.items() if n.startswith("test_fact")}
            plain = {n: s for n, s in hidden.items() if not n.startswith("test_fact")}
            if not facts or not plain:
                problems.append(f"{variant}: missing tests {hidden} {out[-400:]}")
                continue
            if variant == "ref":
                vcode, vis, vout = pytest(repo, "tests", env)
                if vcode != 0 or hcode != 0:
                    problems.append(f"ref fails: visible={vis} hidden={hidden}\n{out[-800:]}")
            else:
                if any(s != "PASSED" for s in plain.values()):
                    problems.append(f"default fails plain tests: {plain}")
                if any(s == "PASSED" for s in facts.values()):
                    problems.append(f"default passes a fact test: {facts}")
    return problems


if __name__ == "__main__":
    bad = 0
    for i in range(1, 25):
        tid = f"S{i:02d}"
        probs = check(tid)
        print(tid, "ok" if not probs else "PROBLEM")
        for p in probs:
            print("   ", p)
        bad += bool(probs)
    print("problems:", bad)
