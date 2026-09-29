from app.state import save, load
from app.recovery import recover

print("=== TESTE DE REINÍCIO E RECUPERAÇÃO ===")

save({
    "agent": "ULTRON-EXPERIMENT",
    "running": True,
    "phase": "recovery-test",
    "counter": 42,
})

print("Estado salvo.")

state = load()
if state is None:
    raise SystemExit("ERRO: estado não foi salvo")

print("Estado encontrado:", state)

result = recover()

if not result["recovered"]:
    raise SystemExit("ERRO: recuperação falhou")

recovered = result["state"]["state"]

if recovered["counter"] != 42:
    raise SystemExit("ERRO: estado recuperado incorreto")

print("Estado recuperado corretamente.")
print("REINÍCIO + RECUPERAÇÃO OK")
