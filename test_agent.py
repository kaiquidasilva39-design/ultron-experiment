from app.agent import agent

print("=== TESTE DO AGENTE ===")

print(agent.start())

print("\nProcessamento:")
print(agent.think("Aprender sobre inteligência artificial."))

print("\nPesquisa:")
result = agent.research("https://example.com")
print(result["url"])
print(result["length"])

print("\nMemórias:")
for item in agent.memories(10):
    print(item)

print("\nEstado final:")
print(agent.status())
