from app.brain import brain
from app.logger import logger
from app.memory import remember, recall, count
from app.learning import record_experiment
from app.cognition import (
    perceive,
    set_goal,
    update_internal_state,
    learn_from_experience,
    reflect,
    decide,
    adapt,
    self_control,
    cognitive_cycle,
)
from app.ai.local_model import ask, available


class Agent:

    def status(self):
        return {
            "memory_count": count(),
            "ai_available": available(),
        }

    def perceive(self, text):
        return perceive(text)

    def remember(self, kind, content):
        return remember(kind, content)

    def memories(self, limit=20):
        return recall(limit)

    def learn(self, title, action, result, score=None):
        return record_experiment(
            title, action, result, score
        )

    def set_goal(self, goal):
        return set_goal(goal)

    def update_state(self, **updates):
        return update_internal_state(**updates)

    def learn_experience(
        self, title, action, result, score=None
    ):
        return learn_from_experience(
            title, action, result, score
        )

    def reflect(self, goal, result, score=None):
        return reflect(goal, result, score)

    def decide(
        self,
        options,
        confidence=0.5,
        uncertainty=0.5,
    ):
        return decide(
            options,
            confidence,
            uncertainty,
        )

    def adapt(self, evaluation):
        return adapt(evaluation)

    def self_control(self, *args, **kwargs):
        return self_control(*args, **kwargs)

    def cognitive_cycle(self, content, goal=None):
        return cognitive_cycle(content, goal)

    def ai(self, prompt, system=None):
        response = ask(
            prompt,
            system=system if system else (
                "Você é o núcleo de inteligência artificial "
                "do ULTRON-EXPERIMENT. "
                "Responda em português do Brasil."
            ),
        )

        remember("ai_response", response)

        logger.info(
            "Resposta produzida pelo núcleo de IA."
        )

        return response

    def ai_with_memory(self, prompt, memory_limit=10):
        memories = self.memories(memory_limit)

        context = []

        for item in memories:
            context.append(
                f"[{item.get('kind', 'memory')}] "
                f"{item.get('content', '')}"
            )

        memory_context = "\n".join(context)

        full_prompt = (
            "Contexto de memória:\n"
            f"{memory_context}\n\n"
            "Solicitação atual:\n"
            f"{prompt}"
        )

        return self.ai(full_prompt)

    def ai_cognitive_cycle(self, content, goal=None):
        cognition = self.cognitive_cycle(
            content,
            goal,
        )

        response = self.ai_with_memory(content)

        return {
            "cognition": cognition,
            "response": response,
        }

    def start(self):
        logger.info(
            "Agente ULTRON iniciado."
        )
        return self.status()

    def stop(self):
        logger.info(
            "Agente ULTRON encerrado."
        )
        return True


agent = Agent()
