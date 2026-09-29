from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "app",
    "config",
    "data",
    "logs",
    "sandbox",
    "backups",
    "run.py",
    "service.py",
    "backup.sh",
    "verify.py",
    "VERSION",
]

print("=== CHECK DE DEPLOY ===")

missing = []

for item in required:
    path = ROOT / item

    if path.exists():
        print("OK   ", item)
    else:
        print("FALTA ", item)
        missing.append(item)

if missing:
    print("\nDeploy incompleto.")
    raise SystemExit(1)

print("\nDEPLOY CHECK OK")
