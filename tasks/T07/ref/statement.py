"""Account statement."""


def statement(acct):
    return [f"{k} {a}" for k, a in acct.history()] + [f"balance {acct.balance()}"]
