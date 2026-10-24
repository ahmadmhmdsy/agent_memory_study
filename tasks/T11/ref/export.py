"""CSV export."""


def to_csv(contacts):
    out = ["name,phone"]
    for n in contacts.names():
        q = f'"{n}"' if "," in n else n
        out.append(f"{q},{contacts.phone(n)}")
    return out
