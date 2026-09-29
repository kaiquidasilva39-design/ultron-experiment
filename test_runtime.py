from app.runtime import runtime_info, checkpoint

print("=== TESTE DE RUNTIME ===")

info = runtime_info()

print("Agente:", info["agent"])
print("Ambiente:", info["environment"])
print("Diretório:", info["root"])

checkpoint()

print("CHECKPOINT OK")
