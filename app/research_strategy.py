from app.research_compare import compare_research
from app.memory import remember


def choose_research_strategy(goal, limit=5):
    result = compare_research(goal, limit)

    strategy = result["selected"]
    scores = result["strategies"]

    remember(
        "research_strategy",
        f"Objetivo={goal} | escolhida={strategy} | desempenho={scores}"
    )

    return {
        "goal": goal,
        "strategy": strategy,
        "scores": scores,
        "results": result["results"],
    }
