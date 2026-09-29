import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMORY_FILE = ROOT / "data" / "memory" / "episodic.jsonl"


STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da",
    "dos", "das", "e", "em", "no", "na", "para", "por",
    "com", "que", "se", "ao", "aos", "é", "ser", "ou",
    "como"
}


def keywords(text):
    words = re.findall(r"\b[\wÀ-ÿ]+\b", str(text).lower())
    return {
        w for w in words
        if w not in STOPWORDS and len(w) > 2
    }


def search_memory(query, limit=10):
    if not MEMORY_FILE.exists():
        return []

    query_words = keywords(query)
    scored = []

    with MEMORY_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            content = json.dumps(item, ensure_ascii=False)
            memory_words = keywords(content)
            score = len(query_words & memory_words)

            if score > 0:
                scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in scored[:limit]]
