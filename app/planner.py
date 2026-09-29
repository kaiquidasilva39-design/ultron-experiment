import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_FILE = ROOT / "data" / "plans.jsonl"


def create_plan(goal, steps):
    PLAN_FILE.parent.mkdir(parents=True, exist_ok=True)

    plan = {
        "goal": goal,
        "steps": [
            {"index": i + 1, "action": step, "status": "pending"}
            for i, step in enumerate(steps)
        ],
    }

    with PLAN_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(plan, ensure_ascii=False) + "\n")

    return plan


def choose_steps(goal, previous_experiments=None):
    previous_experiments = previous_experiments or []

    steps = [
        "Analisar o objetivo",
        "Consultar experiências anteriores",
        "Identificar informações relevantes",
    ]

    if previous_experiments:
        steps.append("Comparar com resultados anteriores")
    else:
        steps.append("Estabelecer uma linha de referência")

    steps.append("Executar processamento controlado")
    steps.append("Registrar resultado para aprendizado futuro")

    return steps


def recent(limit=5):
    if not PLAN_FILE.exists():
        return []

    lines = PLAN_FILE.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines[-limit:]]
