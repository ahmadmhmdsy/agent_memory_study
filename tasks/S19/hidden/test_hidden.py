from grades import clamp, mean, highest, letter, spread


def test_basics():
    assert clamp(-1) == 0 and mean([2, 4]) == 3 and highest([1, 7, 3]) == 7
    assert spread([4, 9, 1]) == 8


def test_fact_letter_bands():
    got = [letter(s) for s in (100, 85, 84, 70, 69, 55, 54, 0)]
    assert got == ["A", "A", "B", "B", "C", "C", "F", "F"]
