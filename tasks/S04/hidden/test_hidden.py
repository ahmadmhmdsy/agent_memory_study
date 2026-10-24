import pytest
import inventory
from inventory import Inventory


def test_add_total():
    inv = Inventory()
    inv.add_stock("pen", 3)
    inv.add_stock("pen", 2)
    inv.add_stock("cup", 1)
    assert inv.quantity("pen") == 5 and inv.quantity("x") == 0
    assert inv.total_items() == 6


def test_remove_ok():
    inv = Inventory()
    inv.add_stock("pen", 3)
    inv.remove_stock("pen", 2)
    assert inv.quantity("pen") == 1


def test_fact_inventory_error():
    err = inventory.InventoryError
    assert issubclass(err, Exception) and not issubclass(err, (ValueError, KeyError, LookupError))
    inv = Inventory()
    inv.add_stock("pen", 1)
    with pytest.raises(err):
        inv.remove_stock("pen", 5)
    assert inv.quantity("pen") == 1
