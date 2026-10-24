"""Claim summaries and CSV export."""
import csv

from payout import payout


def summary(claims, cid):
    _, _, incident, filed = claims.get(cid)
    return [f"claim: {cid}", f"payout: {payout(claims, cid)}", f"days: {(filed - incident).days}"]


def export_claims(claims, path):
    ids = sorted(claims.ids(), key=lambda k: (claims.get(k)[3], k))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "number", "payout"])
        for k in ids:
            w.writerow([k, claims.get(k)[0], payout(claims, k)])
