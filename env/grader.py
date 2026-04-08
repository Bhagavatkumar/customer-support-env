def grade(task, actions):
    """
    Evaluates agent response for a given task.

    Ensures:
    - Clear keyword-based grading (validator-friendly)
    - Stable reward signal
    - Strict score range (0,1)
    """

    # Combine all action content
    content = " ".join([a.get("content", "") for a in actions]).lower()

    score = 0.0

    # Strong keyword matching (primary signal)
    for kw in task.get("solution_keywords", []):
        if kw in content:
            score += 0.5

    #  Small efficiency bonus (prevents zero scores)
    if len(actions) <= 2:
        score += 0.2

    #  Ensure strictly between (0,1)
    score = max(0.01, min(score, 0.99))

    return score
