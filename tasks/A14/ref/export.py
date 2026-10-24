"""Job tickets and CSV export."""
import csv

from pricing import price


def ticket(jobs, jid):
    _, pages, _, _, due = jobs.get(jid)
    return [f"job: {jid}", f"pages: {pages}", f"due: {due.isoformat()}"]


def export_jobs(jobs, path):
    ids = sorted(jobs.ids(), key=lambda k: (jobs.get(k)[4], k))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "customer", "pages", "price"])
        for k in ids:
            c, pages, _, _, _ = jobs.get(k)
            w.writerow([k, c, pages, price(jobs, k)])
