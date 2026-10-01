from app.agent import agent
from app.cycle import run_cycle
from app.improvement import generate_improvement_proposals
from app.improvement_experiment import create_experiments, run_experiment
from app.improvement_evaluator import evaluate_improvement
from app.improvement_manager import select_improvements
from app.learning import recent_strategies


def run_autonomous_cycle(goal):
    print("=== V5 CICLO AUTÔNOMO ===")

    previous_strategies = recent_strategies(10)

    cognition = agent.cognition(
        f"""
Executar ciclo autônomo para o objetivo: {goal}

Estratégias aprendidas em ciclos anteriores:
{previous_strategies}
""",
        goal=goal,
    )

    cycle = run_cycle(goal)

    # O ciclo já consulta experiências e memórias.
    # Mantemos esses dados disponíveis para o estágio cognitivo.
    history_context = {
        "previous_strategies": previous_strategies,
        "previous_experiments": cycle.get(
            "previous_experiments",
            []
        ),
        "related_memories": cycle.get(
            "related_memories",
            []
        ),
    }

    proposals = generate_improvement_proposals(cycle)
    print("Propostas:", len(proposals))

    experiments = create_experiments(proposals)
    print("Experimentos:", len(experiments))

    experiment_results = [
        run_experiment(experiment, goal)
        for experiment in experiments
    ]

    evaluations = evaluate_improvement(
        experiment_results,
        cycle["research"],
    )

    decisions = select_improvements(evaluations)

    decision_options = []

    if decisions.get("change_allowed"):
        for item in decisions.get("accepted", []):
            relative_change = float(
                item.get("relative_change", 0.0)
            )

            benefit = max(
                0.0,
                min(1.0, relative_change),
            )

            risk = max(
                0.0,
                min(1.0, 0.2 - (benefit * 0.1)),
            )

            decision_options.append({
                "name": f"melhoria_{item.get('id', len(decision_options) + 1)}",
                "benefit": benefit,
                "risk": risk,
                "relative_change": relative_change,
            })

    cognitive_decision = agent.decide(
        decision_options,
        confidence=agent.internal_state().get("confidence", 0.5),
        uncertainty=agent.internal_state().get("uncertainty", 0.5),
    )

    decision_learning = agent.record_decision_learning(
        decision=cognitive_decision,
        context={
            "goal": goal,
            "evaluations": evaluations,
            "improvement_decisions": decisions,
            "options": decision_options,
        },
    )

    decision_result = agent.record_decision_result(
        decision=cognitive_decision,
        result={
            "evaluations": evaluations,
            "improvement_decisions": decisions,
            "selected_options": decision_options,
        },
        score=cycle.get(
            "evaluation",
            {}
        ).get("score", 0.0),
    )

    decision_history = agent.recent_decision_results(limit=5)

    cycle_score = cycle.get(
        "evaluation",
        {}
    ).get("score", 0.0)

    cognitive_learning = agent.learn(
        title="Ciclo autônomo",
        action=goal,
        result={
            "evaluation": cycle.get("evaluation", {}),
            "decisions": decisions,
        },
        score=cycle_score,
    )

    cognitive_reflection = agent.reflect(
        goal=goal,
        result={
            "evaluation": cycle.get("evaluation", {}),
            "decisions": decisions,
        },
        score=cycle_score,
    )

    adaptation_evaluation = dict(
        cycle.get(
            "evaluation",
            {
                "score": cycle_score,
                "trend": "baseline",
            }
        )
    )

    adaptation_evaluation["decision_history"] = decision_history

    cognitive_adaptation = agent.adapt(
        adaptation_evaluation
    )

    return {
        "cognition": cognition,
        "history_context": history_context,
        "cycle": cycle,
        "proposals": proposals,
        "experiments": experiments,
        "experiment_results": experiment_results,
        "evaluations": evaluations,
        "decisions": decisions,
        "cognitive_decision": cognitive_decision,
        "decision_learning": decision_learning,
        "decision_result": decision_result,
        "decision_history": decision_history,
        "cognitive_learning": cognitive_learning,
        "cognitive_reflection": cognitive_reflection,
        "cognitive_adaptation": cognitive_adaptation,
    }

