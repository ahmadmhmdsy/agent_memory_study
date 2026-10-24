def write_results(quiz, path):
    with open(path, "w", encoding="utf8") as f:
        f.write(f"Quiz: {quiz.title} ({len(quiz.qs)} questions)\n")
        for n in quiz.players():
            f.write(f"{round(quiz.percent(n))}% - {n}\n")
