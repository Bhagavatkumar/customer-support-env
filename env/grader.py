def grade(task, actions):
    content = " ".join([a.get("content", "") for a in actions]).lower()

    #  keyword match → high score
    for kw in task.get("solution_keywords", []):
        if kw in content:
            return 0.8

    #  fallback → still valid task
    return 0.5
