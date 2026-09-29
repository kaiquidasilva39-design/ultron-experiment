from app.final_runtime import (
    run_final_cycle,
    STATE_FILE,
    HISTORY_FILE,
)
import json

print("=== V5 FINAL TEST ===")

result = run_final_cycle("teste final do sistema")

assert result["status"] == "completed"
assert result["result"]["cycle"]["research"]
assert result["result"]["proposals"]
assert result["result"]["experiments"]
assert result["result"]["evaluations"]

assert STATE_FILE.exists()
assert HISTORY_FILE.exists()

state = json.loads(
    STATE_FILE.read_text(encoding="utf-8")
)

assert state["status"] == "completed"

print("Ciclo: OK")
print("Persistência: OK")
print("Estado: OK")
print("Histórico: OK")
print("Pesquisa:",
      len(result["result"]["cycle"]["research"]))
print("Propostas:",
      len(result["result"]["proposals"]))
print("Experimentos:",
      len(result["result"]["experiments"]))
print("Avaliações:",
      len(result["result"]["evaluations"]))
print(
    "Mudança permitida:",
    result["result"]["decisions"]["change_allowed"]
)

print("=== V5 100% OK ===")
print("=== ULTRON-EXPERIMENT FINALIZADO ===")
