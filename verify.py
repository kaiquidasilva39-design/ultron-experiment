from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

required = [
    "run.py",
    "backup.sh",
    "app/agent.py",
    "app/brain.py",
    "app/memory.py",
    "app/research.py",
    "app/learning.py",
    "app/planner.py",
    "app/executor.py",
    "app/cycle.py",
    "app/state.py",
    "config/config.py",
]

print("=== VERIFICAÇÃO DO PROJETO ===")

errors = []

for item in required:
    path = ROOT / item

    if path.exists():
        print("OK   ", item)
    else:
        print("FALHA", item)
        errors.append(item)

config_file = ROOT / "config" / "config.py"

if config_file.exists():
    print("Configuração: OK")

state_file = ROOT / "data" / "state.json"

if state_file.exists():
    try:
        json.loads(state_file.read_text(encoding="utf-8"))
        print("Estado: OK")
    except Exception:
        print("Estado: inválido")
        errors.append("data/state.json")

if errors:
    print("\nFalhas encontradas:", errors)
    raise SystemExit(1)

print("\nVERIFICAÇÃO OK")
