from app.memory import remember
from app.research_compare import compare_research


def create_experiments(proposals):
    experiments = []

    for i, proposal in enumerate(proposals, 1):
        experiment = {
            "id": i,
            "area": proposal["area"],
            "problem": proposal["problem"],
            "proposal": proposal["proposal"],
            "status": "ready",
        }

        experiments.append(experiment)

    remember(
        "improvement_experiments",
        f"Experimentos criados: {len(experiments)}"
    )

    return experiments


def run_experiment(experiment, goal):
    if experiment["area"] != "research":
        return {
            **experiment,
            "status": "skipped",
            "reason": "Área ainda não possui executor específico",
        }

    try:
        result = compare_research(goal, 5)

        return {
            **experiment,
            "status": "completed",
            "strategies": result["strategies"],
            "selected": result["selected"],
            "results": len(result["results"]),
        }

    except Exception as e:
        return {
            **experiment,
            "status": "failed",
            "reason": str(e),
        }
