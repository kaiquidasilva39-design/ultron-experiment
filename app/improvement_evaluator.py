from app.memory import remember


def evaluate_improvement(experiment_results, baseline_results):
    baseline_count = len(baseline_results)
    evaluations = []

    for result in experiment_results:
        if result.get("status") != "completed":
            evaluations.append({
                "id": result["id"],
                "decision": "reject",
                "reason": "Experimento não concluído",
            })
            continue

        new_count = result.get("results", 0)

        if new_count > baseline_count:
            decision = "candidate"
            reason = "A nova estratégia produziu mais resultados."
        elif new_count == baseline_count:
            decision = "neutral"
            reason = "A nova estratégia produziu a mesma quantidade."
        else:
            decision = "reject"
            reason = "A nova estratégia produziu menos resultados."

        evaluations.append({
            "id": result["id"],
            "decision": decision,
            "baseline": baseline_count,
            "new_results": new_count,
            "reason": reason,
        })

    remember(
        "improvement_evaluation",
        f"Experimentos avaliados: {len(evaluations)}"
    )

    return evaluations
