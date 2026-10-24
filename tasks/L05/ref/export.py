def export_loans(loans, path):
    with open(path, "w", newline="") as f:
        f.write("isbn,member,due\n")
        for i in sorted(loans.loans):
            f.write(f"{i},{loans.holder(i)},{loans.due(i).isoformat()}\n")
