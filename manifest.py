from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent

files = [
    "run.py",
    "service.py",
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
    "app/runtime.py",
    "app/recovery.py",
    "health_check.py",
    "config/config.py",
]

manifest = {
    "name": "ULTRON-EXPERIMENT",
    "version": "0.1-local",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "files": {},
}

for filename in files:
    path = ROOT / filename

    if not path.exists():
        raise SystemExit(f"Arquivo ausente: {filename}")

    digest = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    manifest["files"][filename] = {
        "sha256": digest,
        "size": path.stat().st_size,
    }

output = ROOT / "data" / "manifest.json"
output.write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("Manifesto criado:", output)
print("Arquivos verificados:", len(files))
print("MANIFESTO OK")
