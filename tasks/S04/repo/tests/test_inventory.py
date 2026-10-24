from inventory import Inventory


def test_add():
    inv = Inventory()
    inv.add_stock("pen", 3)
    assert inv.quantity("pen") == 3
