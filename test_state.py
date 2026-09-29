from app.state import save, load

print("=== TESTE DE PERSISTÊNCIA ===")

saved = save({
    "agent": "ULTRON-EXPERIMENT",
    "running": True,
    "version": "0.1",
})

print("Estado salvo:", saved)

restored = load()

print("Estado recuperado:", restored)

if restored is None:
    raise SystemExit("ERRO: recuperação falhou")

print("PERSISTÊNCIA OK")
