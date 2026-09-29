from app.agent import agent
from app.planner import create_plan, choose_steps
from app.executor import execute_plan
from app.learning import record_experiment, recent
from app.evaluator import evaluate_results
from app.memory_search import search_memory
from app.adaptation import suggest_adjustment
from app.research_strategy import choose_research_strategy


def run_cycle(goal, research_url=None):
    print("=== CICLO AUTÔNOMO CONTROLADO ===")

    previous = recent(5)
    related_memories = search_memory(goal, limit=10)

    print("0. Experiências anteriores:", len(previous))
    print("0.1. Memórias relacionadas:", len(related_memories))

    agent.observe(f"Objetivo recebido: {goal}")
    print("1. Observação registrada")

    if research_url:
        research = agent.research(research_url)
        strategy = "direct_url"
        print("2. Pesquisa direta:", research["url"])
    else:
        selected = choose_research_strategy(goal, 5)
        research = selected["results"]
        strategy = selected["strategy"]

        for item in research:
            title = item.get("title", "sem título")
            snippet = item.get("snippet", "")
            agent.observe(
                f"Conhecimento pesquisado: {title} — {snippet}"
            )

        print("2. Pesquisa automática:", len(research), "resultados")
        print("2.1. Estratégia escolhida:", strategy)
        print("2.2. Desempenho:", selected["scores"])

    thought = agent.think(
        str({
            "goal": goal,
            "previous_experiments": previous,
            "related_memories": related_memories,
            "research_strategy": strategy,
        })
    )

    print("3. Processamento concluído")

    steps = choose_steps(
        goal,
        previous,
        related_memories
    )

    plan = create_plan(goal, steps)

    print("4. Plano criado")

    results = execute_plan(plan)

    print("5. Execução concluída:", len(results), "etapas")

    evaluation = evaluate_results(results, previous)
    adaptation = suggest_adjustment(evaluation)

    print(
        "6. Avaliação:",
        evaluation["score"],
        evaluation["trend"]
    )

    print(
        "6.1. Adaptação:",
        adaptation["action"],
        "-",
        adaptation["reason"]
    )

    record_experiment(
        title="Ciclo completo",
        action=goal,
        result=f"{len(results)} etapas executadas; estratégia={strategy}",
        score=evaluation["score"],
    )

    print("7. Resultado registrado")

    return {
        "goal": goal,
        "research": research,
        "research_strategy": strategy,
        "thought": thought,
        "previous_experiments": previous,
        "related_memories": related_memories,
        "plan": plan,
        "results": results,
        "evaluation": evaluation,
        "adaptation": adaptation,
    }
