from app.agent import agent
from app.state import load
from app.recovery import recover

def check():
    status = agent.status()
    state = load()
    recovery = recover()

    checks = {
        "agent": bool(status.get("name")),
        "memory_state": state is not None,
        "recovery": recovery.get("recovered", False),
    }

    return {
        "healthy": all(checks.values()),
        "checks": checks,
    }

if __name__ == "__main__":
    print("=== HEALTH CHECK ===")

    result = check()

    for name, ok in result["checks"].items():
        print(f"{name}: {'OK' if ok else 'FALHA'}")

    print("HEALTHY:", result["healthy"])

    if not result["healthy"]:
        raise SystemExit(1)

    print("HEALTH CHECK OK")
