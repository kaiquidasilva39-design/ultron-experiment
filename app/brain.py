import re
from collections import Counter
from app.memory import remember


STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "e", "em", "no", "na",
    "nos", "nas", "para", "por", "com", "que", "se", "ao",
    "aos", "é", "ser", "foi", "ou", "como"
}


class Brain:
    def process(self, text):
        text = str(text).strip()

        words = re.findall(r"\b[\wÀ-ÿ]+\b", text.lower())
        useful = [w for w in words if w not in STOPWORDS and len(w) > 2]

        frequencies = Counter(useful)

        result = {
            "input": text,
            "type": "context_analysis",
            "length": len(text),
            "word_count": len(words),
            "keywords": [word for word, _ in frequencies.most_common(10)],
            "keyword_frequency": dict(frequencies.most_common(10)),
        }

        remember(
            "thought",
            f"Análise: {result['keywords']}"
        )

        return result


brain = Brain()
