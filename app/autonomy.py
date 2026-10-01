import json
import time
from pathlib import Path

from app.agent import agent
from app.cycle import run_cycle


class AutonomousController:
    def __init__(self, max_iterations=10, delay=0):
        self.max_iterations = max(1, int(max_iterations))
        self.delay = max(0, int(delay))
        self.running = False
        self.history = []
        self.goal_queue = []

        self.state_file = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "autonomy_state.json"
        )
        self.state_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def add_goal(self, goal, priority=0, risk=0.0):
        goal = str(goal).strip()

        if not goal:
            return {"added": False, "reason": "Objetivo vazio"}

        risk = max(
            0.0,
            min(1.0, float(risk)),
        )

        item = {
            "goal": goal,
            "priority": int(priority),
            "risk": risk,
        }

        self.goal_queue.append(item)

        self.goal_queue.sort(
            key=lambda item: item.get("priority", 0),
            reverse=True,
        )

        return {
            "added": True,
            "goal": goal,
            "priority": item["priority"],
            "queue_size": len(self.goal_queue),
        }

    def next_goal(self):
        if not self.goal_queue:
            return None

        item = self.goal_queue.pop(0)

        if isinstance(item, dict):
            return item.get("goal")

        return item

    def reorder_by_internal_state(
        self,
        confidence=0.5,
        uncertainty=0.5,
        risk=0.0,
    ):
        for item in self.goal_queue:
            if isinstance(item, dict):
                item["effective_priority"] = self.effective_priority(
                    priority=item.get("priority", 0),
                    confidence=confidence,
                    uncertainty=uncertainty,
                    risk=item.get("risk", risk),
                )

        self.goal_queue.sort(
            key=lambda item: (
                item.get("effective_priority", 0)
                if isinstance(item, dict)
                else 0
            ),
            reverse=True,
        )

        return self.goal_queue

    def adapt_queue_risk(self, score):
        score = max(
            0.0,
            min(1.0, float(score)),
        )

        for item in self.goal_queue:
            if not isinstance(item, dict):
                continue

            current_risk = max(
                0.0,
                min(
                    1.0,
                    float(item.get("risk", 0.0)),
                ),
            )

            if score < 0.5:
                current_risk += 0.1
            elif score > 0.8:
                current_risk -= 0.1

            item["risk"] = round(
                max(0.0, min(1.0, current_risk)),
                4,
            )

        return self.goal_queue

    def effective_priority(
        self,
        priority=0,
        confidence=0.5,
        uncertainty=0.5,
        risk=0.0,
    ):
        priority = float(priority)
        confidence = max(0.0, min(1.0, float(confidence)))
        uncertainty = max(0.0, min(1.0, float(uncertainty)))
        risk = max(0.0, min(1.0, float(risk)))

        value = (
            priority
            + confidence
            - uncertainty
            - risk
        )

        return round(value, 4)

    def load_state(self):
        if not self.state_file.exists():
            return None

        try:
            state = json.loads(
                self.state_file.read_text(
                    encoding="utf-8"
                )
            )

            queue = state.get("goal_queue", [])

            if isinstance(queue, list):
                normalized = []

                for item in queue:
                    if isinstance(item, dict):
                        goal = str(item.get("goal", "")).strip()

                        if goal:
                            normalized.append({
                                "goal": goal,
                                "priority": int(
                                    item.get("priority", 0)
                                ),
                                "risk": max(
                                    0.0,
                                    min(
                                        1.0,
                                        float(
                                            item.get("risk", 0.0)
                                        ),
                                    ),
                                ),
                            })

                    elif str(item).strip():
                        normalized.append({
                            "goal": str(item).strip(),
                            "priority": 0,
                        })

                normalized.sort(
                    key=lambda item: item.get("priority", 0),
                    reverse=True,
                )

                self.goal_queue = normalized

            return state
        except (json.JSONDecodeError, OSError):
            return None

    def execute(self, goal):
        self.running = True

        saved = self.load_state()

        if (
            saved
            and saved.get("goal") == goal
            and isinstance(saved.get("history"), list)
        ):
            self.history = list(saved["history"])
            start_iteration = (
                int(saved.get("iteration", len(self.history))) + 1
            )
        else:
            self.history = []
            start_iteration = 1

        for iteration in range(
            start_iteration,
            self.max_iterations + 1
        ):
            if not self.running:
                break

            try:
                result = run_cycle(goal)

                entry = {
                    "iteration": iteration,
                    "status": "completed",
                    "score": result.get(
                        "evaluation", {}
                    ).get("score", 0.0),
                    "trend": result.get(
                        "evaluation", {}
                    ).get("trend"),
                }

            except Exception as exc:
                entry = {
                    "iteration": iteration,
                    "status": "failed",
                    "error": str(exc),
                }

            self.history.append(entry)

            self.state_file.write_text(
                json.dumps(
                    {
                        "goal": goal,
                        "running": self.running,
                        "iteration": iteration,
                        "history": self.history,
                        "goal_queue": self.goal_queue,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            if entry["status"] == "completed":
                score = float(entry.get("score", 0.0))
                trend = entry.get("trend")

                agent.learn(
                    title="Autonomia",
                    action=goal,
                    result=f"ciclo {iteration} concluído",
                    score=score,
                )

                agent.reflect(
                    goal=goal,
                    result=entry,
                    score=score,
                )

                agent.adapt({
                    "score": score,
                    "trend": trend,
                    "decision_history": agent.recent_decision_results(5),
                })

            if self.delay:
                time.sleep(self.delay)

        self.running = False

        self.state_file.write_text(
            json.dumps(
                {
                    "goal": goal,
                    "running": False,
                    "iteration": len(self.history),
                    "history": self.history,
                    "goal_queue": self.goal_queue,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return {
            "goal": goal,
            "iterations": len(self.history),
            "history": self.history,
        }

    def execute_queue(self):
        results = []

        while self.goal_queue:
            if not self.goal_queue:
                break

            internal_state = agent.internal_state()

            self.reorder_by_internal_state(
                confidence=internal_state.get(
                    "confidence",
                    0.5,
                ),
                uncertainty=internal_state.get(
                    "uncertainty",
                    0.5,
                ),
                risk=0.0,
            )

            self.state_file.write_text(
                json.dumps(
                    {
                        "goal": None,
                        "running": False,
                        "iteration": len(self.history),
                        "history": self.history,
                        "goal_queue": self.goal_queue,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            goal = self.next_goal()

            if goal is None:
                break

            result = self.execute(goal)

            latest_history = result.get(
                "history",
                [],
            )

            if latest_history:
                latest_score = float(
                    latest_history[-1].get(
                        "score",
                        0.0,
                    )
                )

                self.adapt_queue_risk(
                    latest_score
                )

            results.append(result)

            self.state_file.write_text(
                json.dumps(
                    {
                        "goal": goal,
                        "running": self.running,
                        "iteration": len(self.history),
                        "history": self.history,
                        "goal_queue": self.goal_queue,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

        return {
            "goals_executed": len(results),
            "results": results,
            "remaining_goals": list(self.goal_queue),
        }

    def stop(self):
        self.running = False
        return {"stopped": True}


autonomous_controller = AutonomousController()
