import json
from datetime import datetime, timezone
from pathlib import Path

from app.autonomous_cycle import run_autonomous_cycle

ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIR = ROOT / "data" / "runtime"
STATE_FILE = RUNTIME_DIR / "state.json"
HISTORY_FILE = RUNTIME_DIR / "cycles.jsonl"


def now():
    return datetime.now(timezone.utc).isoformat()


def save_state(state):
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    STATE_FILE.write_text(
        json.dumps(
            state,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def save_history(result):
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                result,
                ensure_ascii=False,
            )
            + "\n"
        )


def run_final_cycle(goal):
    started = now()

    save_state({
        "status": "running",
        "started_at": started,
        "goal": goal,
    })

    try:
        result = run_autonomous_cycle(goal)

        finished = now()

        final_result = {
            "status": "completed",
            "started_at": started,
            "finished_at": finished,
            "goal": goal,
            "result": result,
        }

        save_history(final_result)

        save_state({
            "status": "completed",
            "started_at": started,
            "finished_at": finished,
            "goal": goal,
            "last_change_allowed":
                result["decisions"]["change_allowed"],
        })

        return final_result

    except Exception as exc:
        finished = now()

        error = {
            "status": "failed",
            "started_at": started,
            "finished_at": finished,
            "goal": goal,
            "error": str(exc),
        }

        save_history(error)

        save_state({
            "status": "failed",
            "started_at": started,
            "finished_at": finished,
            "goal": goal,
            "error": str(exc),
        })

        raise
