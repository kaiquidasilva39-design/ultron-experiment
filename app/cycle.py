from app.agent import agent
from app.planner import create_plan
from app.executor import execute_plan
from app.learning import record_experiment


def run_cycle(goal, research_url=None):
    print("=== CICLO AUTÔNOMO CONTROLADO ===")

    observation = f"Objetivo recebido: {goal}"
    agent.observe(observation)

    print("1. Observação registrada")

    if research_url:
        research = agent.research(research_url)
        print("2. Pesquisa concluída:", research["url"])
    else:
        research = None
        print("2. Pesquisa não solicitada")

    thought = agent.think(goal)
    print("3. Processamento concluído")

    plan = create_plan(
        goal,
        [
            "Analisar o objetivo",
            "Organizar as informações",
            "Executar processamento controlado",
            "Registrar resultado",
        ],
    )

    print("4. Plano criado")

    results = execute_plan(plan)

    print("5. Execução concluída:", len(results), "etapas")

    record_experiment(
        title="Ciclo completo",
        action=goal,
        result=f"{len(results)} etapas executadas",
        score=1.0,
    )

    print("6. Resultado registrado")

    return {
        "goal": goal,
        "research": research,
        "thought": thought,
        "plan": plan,
        "results": results,
    }
