from app.agent import agent
from app.cycle import run_cycle
from app.state import save, load

print("=== TESTE FINAL INTEGRADO ===")

print("\n[1] Agente")
print(agent.start())

print("\n[2] Memória")
agent.observe("Teste final de integração.")

print("\n[3] Ciclo")
result = run_cycle(
    "Teste final do sistema",
    "https://example.com",
)

print("Ciclo:", result["goal"])
print("Etapas:", len(result["results"]))

print("\n[4] Estado")
save({
    "agent": agent.name,
    "running": agent.running,
    "test": "final",
})

restored = load()

if restored is None:
    raise SystemExit("ERRO: estado não recuperado")

print("Estado recuperado: OK")

print("\n[5] Resultado")
print("TESTE FINAL OK")
