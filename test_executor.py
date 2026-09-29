from app.planner import create_plan
from app.executor import execute_plan

print("=== TESTE DE EXECUÇÃO ===")

plan = create_plan(
    "Teste de execução controlada",
    [
        "Preparar tarefa",
        "Executar processamento",
        "Registrar resultado",
    ],
)

results = execute_plan(plan)

for result in results:
    print(result)

print("\nEtapas concluídas:", len(results))
print("Estado dos passos:")

for step in plan["steps"]:
    print(step)
