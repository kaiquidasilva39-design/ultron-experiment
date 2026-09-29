from app.learning import record_experiment, recent, count

print("=== TESTE DE APRENDIZADO ===")

item = record_experiment(
    title="Teste inicial",
    action="Processar uma observação",
    result="Processamento concluído",
    score=1.0,
)

print("Experiência registrada:")
print(item)

print("\nHistórico:")

for item in recent(10):
    print(item)

print("\nTotal:", count())
