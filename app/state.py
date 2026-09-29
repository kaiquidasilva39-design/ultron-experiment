import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FILE = BASE / "data" / "state.json"


def save(state):
    FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "state": state,
    }

    FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return data


def load():
    if not FILE.exists():
        return None

    try:
        return json.loads(
            FILE.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError:
        return None
