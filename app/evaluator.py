def evaluate_results(results, previous_experiments=None):
    previous_experiments = previous_experiments or []

    total = len(results)
    completed = sum(
        1 for item in results
        if item.get("status") in ("completed", "success", "done")
    )

    score = completed / total if total else 0.0

    previous_scores = [
        item.get("score")
        for item in previous_experiments
        if isinstance(item.get("score"), (int, float))
    ]

    previous_average = (
        sum(previous_scores) / len(previous_scores)
        if previous_scores else None
    )

    if previous_average is None:
        trend = "baseline"
    elif score > previous_average:
        trend = "improved"
    elif score < previous_average:
        trend = "declined"
    else:
        trend = "stable"

    return {
        "score": round(score, 4),
        "completed": completed,
        "total": total,
        "previous_average": previous_average,
        "trend": trend,
    }
