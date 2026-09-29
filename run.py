from app.agent import agent

print("ULTRON-EXPERIMENT")
print("Estado inicial:")
print(agent.status())

agent.start()

print("Estado após iniciar:")
print(agent.status())
