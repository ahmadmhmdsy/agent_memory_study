def fmt_money(cents):
    return f"{cents // 100:,}.{cents % 100:02d}"


def write_statement(ledger, account, path):
    with open(path, "w", encoding="utf8") as f:
        f.write(f"ACCOUNT {account.upper()}\n")
        for c in ledger.history(account):
            f.write(f"{'+' if c > 0 else '-'}{fmt_money(abs(c))}\n")
        f.write(f"Closing balance: ${fmt_money(ledger.balance(account))}\n")
