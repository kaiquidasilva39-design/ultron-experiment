from app.cycle import run_cycle
from app.improvement import generate_improvement_proposals
from app.improvement_experiment import create_experiments, run_experiment
from app.improvement_evaluator import evaluate_improvement
from app.improvement_manager import select_improvements


def run_evolution_cycle(goal):
    cycle = run_cycle(goal)

    proposals = generate_improvement_proposals(cycle)
    experiments = create_experiments(proposals)

    experiment_results = [
        run_experiment(experiment, goal)
        for experiment in experiments
    ]

    evaluations = evaluate_improvement(
        experiment_results,
        cycle["research"],
    )

    decisions = select_improvements(evaluations)

    return {
        "cycle": cycle,
        "proposals": proposals,
        "experiments": experiments,
        "experiment_results": experiment_results,
        "evaluations": evaluations,
        "decisions": decisions,
    }
