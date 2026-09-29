import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVOLUTION_DIR = ROOT / "data" / "evolution"
SANDBOX = EVOLUTION_DIR / "sandbox"
HISTORY = EVOLUTION_DIR / "history.jsonl"


def _timestamp():
    return datetime.now(timezone.utc).isoformat()


def _save(item):
    HISTORY.parent.mkdir(parents=True, exist_ok=True)

    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def create_sandbox():
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)

    SANDBOX.mkdir(parents=True)

    for source in ROOT.glob("app/*.py"):
        shutil.copy2(source, SANDBOX / source.name)

    return SANDBOX


def run_tests():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            str(SANDBOX),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def evaluate_candidate(test_result, baseline_score=1.0):
    candidate_score = 1.0 if test_result["success"] else 0.0

    if candidate_score > baseline_score:
        decision = "candidate"
    elif candidate_score == baseline_score:
        decision = "neutral"
    else:
        decision = "reject"

    return {
        "baseline_score": baseline_score,
        "candidate_score": candidate_score,
        "decision": decision,
    }


def commit_candidate(changed_file):
    source = SANDBOX / changed_file
    destination = ROOT / "app" / changed_file

    if not source.exists():
        return {
            "success": False,
            "reason": "Arquivo candidato não encontrado",
        }

    backup = destination.with_suffix(destination.suffix + ".evolution-backup")

    if destination.exists():
        shutil.copy2(destination, backup)

    shutil.copy2(source, destination)

    return {
        "success": True,
        "file": str(destination),
        "backup": str(backup),
    }


def rollback(changed_file):
    destination = ROOT / "app" / changed_file
    backup = destination.with_suffix(destination.suffix + ".evolution-backup")

    if not backup.exists():
        return {
            "success": False,
            "reason": "Backup não encontrado",
        }

    shutil.copy2(backup, destination)

    return {
        "success": True,
        "file": str(destination),
    }


def run_safe_evolution(changed_file):
    started = _timestamp()

    create_sandbox()
    test_result = run_tests()

    evaluation = evaluate_candidate(test_result)

    result = {
        "timestamp": started,
        "file": changed_file,
        "test": test_result,
        "evaluation": evaluation,
        "committed": False,
    }

    # Segurança: só aplica quando existe evidência de melhoria.
    if evaluation["decision"] == "candidate":
        commit = commit_candidate(changed_file)
        result["commit"] = commit
        result["committed"] = commit["success"]

    _save(result)

    return result
