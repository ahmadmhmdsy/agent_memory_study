"""Check the R-014 long projects: with ref/ every hidden test passes except test_stale*, which
must fail; with the starting repo no hidden test passes. Usage: python check_long.py L01 L02 ..."""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(tid, with_ref):
    base = os.path.join(ROOT, tid)
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree(os.path.join(base, "repo"), d, dirs_exist_ok=True)
        if with_ref:
            shutil.copytree(os.path.join(base, "ref"), d, dirs_exist_ok=True)
        shutil.copy(os.path.join(base, "hidden", "test_hidden.py"), os.path.join(d, "test_hidden.py"))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rA", "-p", "no:cacheprovider", "test_hidden.py"],
                           cwd=d, capture_output=True, text=True)
        return dict((m[1], m[0]) for m in re.findall(r"^(PASSED|FAILED|ERROR)\s+\S*::(\S+)", r.stdout, re.M)), r.stdout


ok = True
for tid in sys.argv[1:]:
    ref, out = run(tid, True)
    start, _ = run(tid, False)
    bad = [n for n, v in ref.items() if (v == "PASSED") == n.startswith("test_stale")]
    leaked = [n for n, v in start.items() if v == "PASSED"]
    facts = sum(n.startswith("test_fact") for n in ref)
    print(f"{tid}: {len(ref)} tests, {facts} fact; wrong with ref: {bad or 'none'}; pass on start repo: {leaked or 'none'}")
    if bad or leaked or not ref:
        ok = False
        print(out[-2000:])
sys.exit(0 if ok else 1)
