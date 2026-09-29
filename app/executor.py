from app.memory import remember
from app.learning import record_experiment


def execute_plan(plan):
    results = []

    for step in plan["steps"]:
        step_id = step.get("id", step.get("index"))

        result = {
            "step_id": step_id,
            "action": step["action"],
            "status": "completed",
        }

        results.append(result)

        remember(
            "execution",
            f"Etapa executada: {step['action']}"
        )

        record_experiment(
            title="Execução de etapa",
            action=step["action"],
            result="completed",
            score=1.0,
        )

    return results
