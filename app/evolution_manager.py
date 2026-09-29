from app.safe_evolution import (
    create_sandbox,
    run_tests,
    evaluate_candidate,
    commit_candidate,
    rollback,
)
from app.memory import remember


def test_candidate(changed_file, baseline_score=1.0):
    create_sandbox()

    test = run_tests()
    evaluation = evaluate_candidate(test, baseline_score)

    result = {
        "file": changed_file,
        "test": test,
        "evaluation": evaluation,
        "applied": False,
    }

    # Só aplica se superar o baseline.
    if evaluation["decision"] == "candidate":
        commit = commit_candidate(changed_file)
        result["commit"] = commit
        result["applied"] = commit["success"]

    remember(
        "evolution_test",
        f"Arquivo={changed_file} | decisão={evaluation['decision']} | aplicado={result['applied']}"
    )

    return result


def rollback_candidate(changed_file):
    result = rollback(changed_file)

    remember(
        "evolution_rollback",
        f"Arquivo={changed_file} | sucesso={result['success']}"
    )

    return result
