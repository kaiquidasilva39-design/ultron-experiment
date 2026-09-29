from app.cycle import run_cycle

result = run_cycle(
    "Aprender sobre inteligência artificial",
    "https://example.com",
)

print("\n=== CICLO FINALIZADO ===")
print("Objetivo:", result["goal"])
print("Etapas:", len(result["results"]))
