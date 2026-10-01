import json
from datetime import datetime, timezone
from pathlib import Path

from app.memory import remember
from app.learning import record_experiment, recent, record_strategy, recent_strategies
from app.ai.local_model import ask

ROOT = Path(__file__).resolve().parent.parent
COGNITION_FILE = ROOT / "data" / "cognition.json"

DEFAULT_STATE = {
    "curiosity": 0.50,
    "confidence": 0.50,
    "doubt": 0.50,
    "interest": 0.50,
    "frustration": 0.00,
    "uncertainty": 0.50,
    "last_goal": None,
    "cycle": 0,
}


def _now():
    return datetime.now(timezone.utc).isoformat()


def load_cognition():
    if not COGNITION_FILE.exists():
        return dict(DEFAULT_STATE)

    try:
        data = json.loads(
            COGNITION_FILE.read_text(encoding="utf-8")
        )
        state = dict(DEFAULT_STATE)
        state.update(data)
        return state
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT_STATE)


def save_cognition(state):
    COGNITION_FILE.parent.mkdir(parents=True, exist_ok=True)

    COGNITION_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return state


def perceive(content):
    text = str(content).strip()

    observation = {
        "timestamp": _now(),
        "content": text,
        "length": len(text),
        "words": len(text.split()),
        "questions": text.count("?"),
        "exclamations": text.count("!"),
        "has_question": "?" in text,
    }

    remember(
        "perception",
        json.dumps(observation, ensure_ascii=False),
    )

    return observation


def set_goal(goal):
    state = load_cognition()

    state["last_goal"] = str(goal)

    save_cognition(state)

    remember("goal", str(goal))

    return {
        "goal": str(goal),
        "status": "active",
    }


def update_internal_state(**updates):
    state = load_cognition()

    for key, value in updates.items():
        if key in DEFAULT_STATE and value is not None:
            state[key] = max(
                0.0,
                min(1.0, float(value)),
            )

    state["cycle"] += 1

    save_cognition(state)

    return state


def learn_from_experience(title, action, result, score=None):
    experience = record_experiment(
        title=title,
        action=action,
        result=result,
        score=score,
    )

    remember(
        "learning",
        json.dumps(experience, ensure_ascii=False),
    )

    return experience


def reflect(goal, result, score=None):
    history = recent(10)

    scores = [
        item.get("score")
        for item in history
        if isinstance(item.get("score"), (int, float))
    ]

    average = (
        sum(scores) / len(scores)
        if scores
        else None
    )

    if score is None:
        conclusion = "Resultado sem avaliação numérica."
    elif average is None:
        conclusion = "Primeira referência disponível."
    elif score > average:
        conclusion = "Resultado acima da referência anterior."
    elif score < average:
        conclusion = "Resultado abaixo da referência anterior."
    else:
        conclusion = "Resultado próximo da referência anterior."

    reflection = {
        "timestamp": _now(),
        "goal": goal,
        "result": result,
        "score": score,
        "previous_average": average,
        "conclusion": conclusion,
    }

    remember(
        "reflection",
        json.dumps(reflection, ensure_ascii=False),
    )

    return reflection


def decide(options, confidence=0.5, uncertainty=0.5):
    if not options:
        return {
            "decision": None,
            "alternatives": [],
            "confidence": 0.0,
            "safe": False,
            "reason": "Nenhuma alternativa disponível.",
        }

    confidence = max(
        0.0,
        min(1.0, float(confidence)),
    )

    uncertainty = max(
        0.0,
        min(1.0, float(uncertainty)),
    )

    evaluated = []

    for index, option in enumerate(options):
        if isinstance(option, str):
            option = {
                "name": option,
                "benefit": 0.5,
                "risk": 0.0,
            }
        else:
            option = dict(option)

        name = option.get(
            "name",
            option.get("action", f"opcao_{index + 1}"),
        )

        benefit = max(
            0.0,
            min(1.0, float(option.get("benefit", 0.5))),
        )

        risk = max(
            0.0,
            min(1.0, float(option.get("risk", 0.0))),
        )

        score = (
            benefit * confidence
            - risk
            - (uncertainty * 0.25)
        )

        evaluated.append({
            "name": name,
            "benefit": benefit,
            "risk": risk,
            "score": round(score, 4),
        })

    evaluated.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    selected = evaluated[0]

    control = self_control(
        confidence=confidence,
        uncertainty=uncertainty,
        risk=selected["risk"],
    )

    decision = {
        "decision": selected["name"] if control["allowed"] else None,
        "alternatives": evaluated,
        "confidence": confidence,
        "safe": control["allowed"],
        "reason": (
            "Alternativa com maior pontuação selecionada."
            if control["allowed"]
            else control["reason"]
        ),
    }

    remember(
        "decision",
        json.dumps(decision, ensure_ascii=False),
    )

    return decision


def record_decision_learning(decision, context=None):
    context = context or {}

    item = {
        "timestamp": _now(),
        "decision": decision,
        "context": context,
    }

    remember(
        "decision_learning",
        json.dumps(item, ensure_ascii=False),
    )

    return item


def recent_decision_results(limit=5):
    """Retorna os resultados de decisões mais recentes."""
    from app.memory import recall

    limit = max(1, int(limit))
    results = []

    for item in reversed(recall(1000000)):
        if item.get("kind") != "decision_result":
            continue

        try:
            results.append(json.loads(item.get("content", "{}")))
        except (json.JSONDecodeError, TypeError):
            continue

        if len(results) >= limit:
            break

    return results


def record_decision_result(decision, result, score=None):
    item = {
        "timestamp": _now(),
        "decision": decision,
        "result": result,
        "score": score,
    }

    remember(
        "decision_result",
        json.dumps(item, ensure_ascii=False),
    )

    return item


def adapt(evaluation):
    score = float(
        evaluation.get("score", 0.0)
    )

    trend = evaluation.get(
        "trend",
        "baseline",
    )

    actions = {
        "improved": "maintain_strategy",
        "declined": "review_strategy",
        "stable": "test_controlled_variation",
        "baseline": "establish_baseline",
    }

    decision_history = evaluation.get(
        "decision_history",
        []
    )

    decision_scores = [
        item.get("score")
        for item in decision_history
        if isinstance(item, dict)
        and isinstance(item.get("score"), (int, float))
    ]

    last_decision = (
        decision_history[0]
        if decision_history
        else None
    )

    last_decision_score = (
        last_decision.get("score")
        if isinstance(last_decision, dict)
        else None
    )

    if isinstance(last_decision_score, (int, float)):
        if last_decision_score < score:
            decision_effect = "positive"
        elif last_decision_score > score:
            decision_effect = "negative"
        else:
            decision_effect = "neutral"
    else:
        decision_effect = "unknown"

    adaptation = {
        "timestamp": _now(),
        "score": score,
        "trend": trend,
        "action": actions.get(
            trend,
            "review_strategy",
        ),
        "decision_influence": {
            "samples": len(decision_history),
            "scored_samples": len(decision_scores),
            "last_score": last_decision_score,
            "effect": decision_effect,
        },
    }

    strategy_record = record_strategy(
        strategy=adaptation["action"],
        reason=(
            f"trend={trend}; "
            f"decision_effect={decision_effect}"
        ),
        score=score,
        trend=trend,
    )

    adaptation["strategy_record"] = strategy_record
    adaptation["previous_strategies"] = recent_strategies(5)

    remember(
        "adaptation",
        json.dumps(adaptation, ensure_ascii=False),
    )

    return adaptation


def self_control(
    confidence,
    uncertainty,
    risk="low",
):
    confidence = max(
        0.0,
        min(1.0, float(confidence)),
    )

    uncertainty = max(
        0.0,
        min(1.0, float(uncertainty)),
    )

    risk = str(risk).lower()

    if risk in {"high", "critical"}:
        allowed = False
        reason = "Ação bloqueada: risco elevado."

    elif uncertainty >= 0.80:
        allowed = False
        reason = "Ação bloqueada: incerteza elevada."

    elif confidence < 0.40:
        allowed = False
        reason = "Ação bloqueada: confiança insuficiente."

    else:
        allowed = True
        reason = "Ação dentro dos limites atuais."

    result = {
        "allowed": allowed,
        "confidence": confidence,
        "uncertainty": uncertainty,
        "risk": risk,
        "reason": reason,
    }

    remember(
        "self_control",
        json.dumps(result, ensure_ascii=False),
    )

    return result


def cognitive_cycle(content, goal=None):
    perception = perceive(content)

    if goal is not None:
        goal_data = set_goal(goal)
    else:
        state = load_cognition()

        goal_data = {
            "goal": state.get("last_goal"),
            "status": (
                "active"
                if state.get("last_goal")
                else "none"
            ),
        }

    state = load_cognition()

    if perception["has_question"]:
        state = update_internal_state(
            curiosity=state["curiosity"] + 0.10,
            interest=state["interest"] + 0.05,
        )

    control = self_control(
        confidence=state["confidence"],
        uncertainty=state["uncertainty"],
        risk="low",
    )

    prompt = f"""
Você é o núcleo de IA local do Micro-Robô ULTRON.

Analise o ciclo atual.

Conteúdo: {content}
Objetivo: {goal_data.get("goal")}
Percepção: {json.dumps(perception, ensure_ascii=False)}
Estado interno: {json.dumps(state, ensure_ascii=False)}
Autocontrole: {json.dumps(control, ensure_ascii=False)}

Responda em português.
Forneça uma análise curta, objetiva e útil para o próximo ciclo.
"""

    try:
        ai_analysis = ask(prompt)
    except Exception as exc:
        ai_analysis = f"IA local indisponível: {type(exc).__name__}: {exc}"

    result = {
        "perception": perception,
        "goal": goal_data,
        "internal_state": state,
        "self_control": control,
        "ai_analysis": ai_analysis,
    }

    remember(
        "cognitive_cycle",
        json.dumps(result, ensure_ascii=False),
    )

    return result

