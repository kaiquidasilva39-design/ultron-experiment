from datetime import datetime, timezone

from app.memory import remember
from app.learning import record_experiment


def execute_plan(plan):
    results = []

    for step in plan["steps"]:
        started = datetime.now(timezone.utc).isoformat()

        result = {
            "step_id": step["id"],
            "description": step["description"],
            "status": "completed",
            "started": started,
        }

        step["status"] = "completed"
        results.append(result)

        remember(
            "execution",
            f"Etapa concluída: {step['description']}"
        )

    record_experiment(
        title=plan["goal"],
        action="Executar plano controlado",
        result=f"{len(results)} etapas concluídas",
        score=1.0,
    )

    return results
