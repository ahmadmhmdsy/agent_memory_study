from board import COLS


def write_export(board, path):
    with open(path, "w", encoding="utf8") as f:
        for c in COLS:
            for i in sorted(board.column(c)):
                f.write(f"{board.title(i)} ({c})\n")
