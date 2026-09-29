from app.web_research import search_web
from app.auto_research import search_public_knowledge
from app.memory import remember


def compare_research(goal, limit=5):
    strategies = {}

    try:
        web = search_web(goal, limit)
        strategies["web_search"] = web
    except Exception as e:
        strategies["web_search"] = []
        remember("research_error", f"web_search: {e}")

    try:
        wiki = search_public_knowledge(goal)
        strategies["wikipedia"] = wiki[:limit]
    except Exception as e:
        strategies["wikipedia"] = []
        remember("research_error", f"wikipedia: {e}")

    scores = {
        name: len(results)
        for name, results in strategies.items()
    }

    selected = max(scores, key=scores.get)

    result = {
        "goal": goal,
        "strategies": scores,
        "selected": selected,
        "results": strategies[selected],
    }

    remember(
        "research_comparison",
        f"Objetivo={goal} | estratégias={scores} | selecionada={selected}"
    )

    return result
