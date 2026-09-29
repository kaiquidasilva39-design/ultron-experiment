from app.memory import remember, recall, count
from app.logger import logger
from app.brain import brain
from app.research import research


class Agent:
    def __init__(self):
        self.name = "ULTRON-EXPERIMENT"
        self.running = False

    def status(self):
        return {
            "name": self.name,
            "running": self.running,
            "memory_items": count(),
        }

    def observe(self, content):
        item = remember("observation", content)
        logger.info("Observação: %s", content)
        return item

    def think(self, text):
        result = brain.process(text)
        logger.info("Processamento concluído")
        return result

    def research(self, url):
        result = research(url)

        remember(
            "research",
            f"Fonte pesquisada: {url}"
        )

        logger.info("Pesquisa concluída: %s", url)
        return result

    def memories(self, limit=20):
        return recall(limit)

    def start(self):
        self.running = True
        self.observe("Agente iniciado.")
        return self.status()

    def stop(self):
        self.running = False
        self.observe("Agente parado.")
        return self.status()


agent = Agent()
