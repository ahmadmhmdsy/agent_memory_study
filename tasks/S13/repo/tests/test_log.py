from log import Logger


def test_new_logger_empty():
    assert Logger().count() == 0
