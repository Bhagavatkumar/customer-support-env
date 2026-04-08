def grade(task, actions):
    content = " ".join([a.get("content", "") for a in actions]).lower()

    # simple deterministic keyword match
    for kw in task.get("solution_keywords", []):
        if kw in content:
            return 0.8  # valid score

    return 0.2  # always non-zero (important)
