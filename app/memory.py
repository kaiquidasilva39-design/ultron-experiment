import json
from datetime import datetime, timezone
from config.config import MEMORY_DIR

MEMORY_DIR.mkdir(parents=True, exist_ok=True)
FILE = MEMORY_DIR / "episodic.jsonl"

def remember(kind, content):
    item = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        "content": content,
    }

    with FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return item

def recall(limit=20):
    if not FILE.exists():
        return []

    lines = FILE.read_text(encoding="utf-8").splitlines()
    items = []

    for line in lines[-limit:]:
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    return items

def count():
    return len(recall(1000000))
