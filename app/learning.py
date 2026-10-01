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


STRATEGY_FILE = BASE / "data" / "learning" / "strategies.jsonl"
STRATEGY_FILE.parent.mkdir(parents=True, exist_ok=True)


def record_strategy(strategy, reason=None, score=None, trend=None):
    item = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "strategy": strategy,
        "reason": reason,
        "score": score,
        "trend": trend,
    }

    with STRATEGY_FILE.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(item, ensure_ascii=False) + "\n"
        )

    return item


def recent_strategies(limit=10):
    if not STRATEGY_FILE.exists():
        return []

    lines = STRATEGY_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    result = []

    for line in lines[-limit:]:
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    return result

RESEARCH_STRATEGY_FILE = BASE / "data" / "learning" / "research_strategies.jsonl"
RESEARCH_STRATEGY_FILE.parent.mkdir(parents=True, exist_ok=True)

def record_research_strategy(strategy, score=None, selected=False):
    item = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "strategy": strategy,
        "score": score,
        "selected": selected,
    }

    with RESEARCH_STRATEGY_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return item


def recent_research_strategies(limit=10):
    if not RESEARCH_STRATEGY_FILE.exists():
        return []

    lines = RESEARCH_STRATEGY_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    result = []

    for line in lines[-limit:]:
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    return result
