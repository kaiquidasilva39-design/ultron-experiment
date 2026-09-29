from app.memory import remember


def select_improvements(evaluations):
    accepted = []
    rejected = []
    neutral = []

    for item in evaluations:
        decision = item.get("decision")

        if decision == "candidate":
            accepted.append(item)
        elif decision == "reject":
            rejected.append(item)
        else:
            neutral.append(item)

    result = {
        "accepted": accepted,
        "rejected": rejected,
        "neutral": neutral,
        "change_allowed": len(accepted) > 0,
    }

    remember(
        "improvement_decision",
        f"Aceitas={len(accepted)} | rejeitadas={len(rejected)} | neutras={len(neutral)}"
    )

    return result
