from app.web_research import search_web
from app.memory import remember

def run_research_experiment(goal, limit=5):
    results = search_web(goal, limit)

    experiment = {
        "goal": goal,
        "strategy": "web_search",
        "results": len(results),
        "items": results,
    }

    remember(
        "research_experiment",
        f"Pesquisa experimental: {goal} | resultados={len(results)}"
    )

    return experiment
