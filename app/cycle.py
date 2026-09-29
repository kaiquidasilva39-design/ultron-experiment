from app.agent import agent
from app.planner import create_plan, choose_steps
from app.executor import execute_plan
from app.learning import record_experiment, recent
from app.evaluator import evaluate_results
from app.auto_research import search_public_knowledge


def run_cycle(goal, research_url=None):
    print("=== CICLO AUTÔNOMO CONTROLADO ===")

    # 1. Recuperar experiências anteriores
    previous = recent(5)
    print("0. Experiências anteriores:", len(previous))

    observation = f"Objetivo recebido: {goal}"
    agent.observe(observation)

    print("1. Observação registrada")

    if research_url:
        research = agent.research(research_url)
        print("2. Pesquisa concluída:", research["url"])
    else:
        research = search_public_knowledge(goal)
        print("2. Pesquisa automática:", len(research), "resultados")

    # 3. Processamento usando o contexto disponível
    context = {
        "goal": goal,
        "previous_experiments": previous,
    }

    thought = agent.think(str(context))
    print("3. Processamento concluído")

    steps = choose_steps(goal, previous)

    plan = create_plan(goal, steps)

    print("4. Plano criado")

    results = execute_plan(plan)

    print("5. Execução concluída:", len(results), "etapas")

    evaluation = evaluate_results(results, previous)

    print(
        "6. Avaliação:",
        evaluation["score"],
        evaluation["trend"]
    )

    record_experiment(
        title="Ciclo completo",
        action=goal,
        result=f"{len(results)} etapas executadas",
        score=evaluation["score"],
    )

    print("7. Resultado registrado")

    return {
        "goal": goal,
        "research": research,
        "thought": thought,
        "previous_experiments": previous,
        "plan": plan,
        "results": results,
        "evaluation": evaluation,
    }
