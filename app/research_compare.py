from app.web_research import search_web
from app.auto_research import search_public_knowledge
from app.memory import remember
from app.learning import recent_research_strategies, record_research_strategy


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

    # Combina desempenho atual com histórico recente.
    history = recent_research_strategies(10)

    history_scores = {
        name: []
        for name in scores
    }

    for item in history:
        strategy = item.get("strategy")
        score = item.get("score")

        if strategy in history_scores and isinstance(score, (int, float)):
            history_scores[strategy].append(score)

    combined_scores = {}

    for name, current_score in scores.items():
        past = history_scores[name]

        if past:
            historical_average = sum(past) / len(past)
        else:
            historical_average = current_score

        combined_scores[name] = (
            current_score * 0.7
            + historical_average * 0.3
        )

    selected = max(combined_scores, key=combined_scores.get)

    # Política adaptativa:
    # quando há empate, tenta uma estratégia diferente da última utilizada.
    if len(scores) > 1:
        best_score = max(scores.values())
        best = [
            name
            for name, value in scores.items()
            if value == best_score
        ]

        previous = recent_research_strategies(10)

        last_research_strategy = None

        for item in reversed(previous):
            strategy = item.get("strategy")
            if strategy in scores:
                last_research_strategy = strategy
                break

        if (
            len(best) > 1
            and last_research_strategy in best
        ):
            alternatives = [
                name
                for name in best
                if name != last_research_strategy
            ]

            if alternatives:
                selected = alternatives[0]

    remember(
        "research_policy",
        f"selecionada={selected} | "
        f"última={last_research_strategy if len(scores) > 1 else None} | "
        f"desempenho={scores}"
    )

    result = {
        "goal": goal,
        "strategies": scores,
        "selected": selected,
        "results": strategies[selected],
    }

    for name, value in scores.items():
        record_research_strategy(
            strategy=name,
            score=value,
            selected=(name == selected),
        )

    remember(
        "research_comparison",
        f"Objetivo={goal} | estratégias={scores} | selecionada={selected}"
    )

    return result
