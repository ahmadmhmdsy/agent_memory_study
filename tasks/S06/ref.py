def make_task(title, done=False):
    return {"title": title, "done": done}


def pending(tasks):
    return [t for t in tasks if not t["done"]]


def write_csv(tasks, path):
    with open(path, "w") as f:
        f.write("title,done\n")
        for t in tasks:
            f.write(f"{t['title']},{'Y' if t['done'] else 'N'}\n")
