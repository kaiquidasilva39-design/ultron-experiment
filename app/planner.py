import json
from datetime import datetime, timezone
from pathlib import Path

from app.memory import remember

BASE = Path(__file__).resolve().parent.parent
FILE = BASE / "data" / "plans.jsonl"

FILE.parent.mkdir(parents=True, exist_ok=True)


def create_plan(goal, steps):
    plan = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "steps": [
            {
                "id": i + 1,
                "description": step,
                "status": "pending",
            }
            for i, step in enumerate(steps)
        ],
    }

    with FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(plan, ensure_ascii=False) + "\n")

    remember("plan", f"Plano criado: {goal}")

    return plan


def recent(limit=10):
    if not FILE.exists():
        return []

    lines = FILE.read_text(encoding="utf-8").splitlines()

    result = []

    for line in lines[-limit:]:
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    return result
