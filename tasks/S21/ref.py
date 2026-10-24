def pad2(n):
    return f"{n:02d}"


def parts(seconds):
    return (seconds // 3600, seconds % 3600 // 60, seconds % 60)


def format_hms(seconds):
    h, m, s = parts(seconds)
    return f"{h}:{pad2(m)}:{pad2(s)}"


def to_seconds(s):
    nums = [int(x) for x in s.split(":")]
    if len(nums) == 2:
        nums = [0] + nums
    h, m, sec = nums
    return h * 3600 + m * 60 + sec


def is_long(seconds):
    return seconds > 3600
