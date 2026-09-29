from app.state import save
from app.recovery import recover

print("=== TESTE DE RECUPERAÇÃO ===")

save({
    "agent": "ULTRON-EXPERIMENT",
    "running": True,
    "checkpoint": "test",
})

result = recover()

print("Recuperado:", result["recovered"])
print("Estado:", result["state"])

if not result["recovered"]:
    raise SystemExit("ERRO: recuperação falhou")

print("RECUPERAÇÃO OK")
