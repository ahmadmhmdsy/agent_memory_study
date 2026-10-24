from phones import check_email, normalize_phone
from names import title_name


class AddressBook:
    def __init__(self):
        self.c = {}

    def add(self, name, phone=None, email=None):
        n = title_name(name)
        if not n:
            raise ValueError("name required")
        if any(k.lower() == n.lower() for k in self.c):
            raise ValueError("duplicate name")
        if phone is None and email is None:
            raise ValueError("phone or email required")
        check_email(email)
        self.c[n] = {"name": n, "phone": normalize_phone(phone) if phone else None, "email": email}

    def get(self, name):
        return dict(self.c[title_name(name)])

    def names(self):
        return sorted(self.c)

    def remove(self, name):
        del self.c[title_name(name)]

    def search(self, text):
        t = text.lower()
        return sorted(n for n, v in self.c.items()
                      if t in n.lower() or (v["email"] and t in v["email"].lower()))

    def count(self):
        return len(self.c)

    def update(self, name, phone=None, email=None):
        v = self.c[title_name(name)]
        if email is not None:
            check_email(email)
            v["email"] = email
        if phone is not None:
            v["phone"] = normalize_phone(phone)
