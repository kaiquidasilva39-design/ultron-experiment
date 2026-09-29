from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

required = [
    "run.py",
    "service.py",
    "backup.sh",
    "verify.py",
    "deploy_check.py",
    "manifest.py",
    "app/agent.py",
    "app/brain.py",
    "app/memory.py",
    "app/research.py",
    "app/learning.py",
    "app/planner.py",
    "app/executor.py",
    "app/cycle.py",
    "app/state.py",
    "app/recovery.py",
    "config/config.py",
    "data/manifest.json",
    "backups/deploy-package.tar.gz",
]

print("=== SERVER READINESS ===")

missing = []

for item in required:
    path = ROOT / item
    if path.exists():
        print("OK   ", item)
    else:
        print("FALTA", item)
        missing.append(item)

print()

if missing:
    print("PREPARAÇÃO: FALHOU")
    sys.exit(1)

print("PREPARAÇÃO PARA SERVIDOR: OK")
