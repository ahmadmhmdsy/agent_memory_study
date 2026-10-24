def find(board, text):
    t = text.lower()
    return sorted(i for i, title in board.titles.items() if t in title.lower())
