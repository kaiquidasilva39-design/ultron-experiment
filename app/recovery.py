from app.state import load, save


def recover():
    state = load()

    if state is None:
        return {
            "recovered": False,
            "reason": "Nenhum estado encontrado",
        }

    return {
        "recovered": True,
        "state": state,
    }


def recovery_checkpoint():
    current = recover()

    if not current["recovered"]:
        save({
            "agent": "ULTRON-EXPERIMENT",
            "running": False,
            "recovery": True,
        })

    return current
