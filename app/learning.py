import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FILE = BASE / "data" / "experiments" / "history.jsonl"

FILE.parent.mkdir(parents=True, exist_ok=True)


def record_experiment(title, action, result, score=None):
    item = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": title,
        "action": action,
        "result": result,
        "score": score,
    }

    with FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return item


def recent(limit=20):
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


def count():
    return len(recent(1000000))
