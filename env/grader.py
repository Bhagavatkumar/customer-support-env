def grade(task, actions):
    content = " ".join([a.get("content", "") for a in actions]).lower()
    
    score = 0.0

    # keyword match
    for kw in task["solution_keywords"]:
        if kw in content:
            score += 0.3

    # efficiency bonus
    if len(actions) <= 3:
        score += 0.2

    # closing action bonus
    if any(a.get("action_type") == "close" for a in actions):
        score += 0.2

    # CRITICAL FIX: strict range (0,1)
    score = max(0.01, min(score, 0.99))

    return score
