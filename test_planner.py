from app.planner import create_plan, recent

print("=== TESTE DO PLANEJADOR ===")

plan = create_plan(
    "Aprender sobre um assunto",
    [
        "Pesquisar informações públicas",
        "Organizar as informações",
        "Registrar o aprendizado",
        "Avaliar o resultado",
    ],
)

print("Objetivo:", plan["goal"])

print("\nEtapas:")

for step in plan["steps"]:
    print(step)

print("\nPlanos registrados:", len(recent()))
