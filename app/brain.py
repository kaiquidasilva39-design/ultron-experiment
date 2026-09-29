from app.memory import remember

class Brain:
    def process(self, text):
        result = {
            "input": text,
            "type": "observation",
            "length": len(text),
        }

        remember(
            "thought",
            f"Processado: {text[:500]}"
        )

        return result

brain = Brain()
