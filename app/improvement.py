from app.memory import remember


def detect_limitations(cycle_result):
    limitations = []

    research = cycle_result.get("research", [])
    evaluation = cycle_result.get("evaluation", {})
    strategy = cycle_result.get("research_strategy")

    if len(research) < 5:
        limitations.append({
            "area": "research",
            "problem": "Poucos resultados de pesquisa",
            "suggestion": "Testar fontes adicionais"
        })

    if evaluation.get("score", 0) < 1:
        limitations.append({
            "area": "execution",
            "problem": "Nem todas as etapas foram concluídas",
            "suggestion": "Revisar execução e tratamento de erros"
        })

    if strategy == "wikipedia":
        limitations.append({
            "area": "research",
            "problem": "Dependência de uma única estratégia vencedora",
            "suggestion": "Adicionar fontes públicas independentes"
        })

    if not limitations:
        limitations.append({
            "area": "optimization",
            "problem": "Nenhuma limitação crítica detectada",
            "suggestion": "Testar uma variação controlada"
        })

    remember(
        "improvement_analysis",
        f"Limitações detectadas: {len(limitations)}"
    )

    return limitations


def generate_improvement_proposals(cycle_result):
    limitations = detect_limitations(cycle_result)

    proposals = []

    for item in limitations:
        proposals.append({
            "area": item["area"],
            "problem": item["problem"],
            "proposal": item["suggestion"],
            "status": "proposed",
        })

    remember(
        "improvement_proposals",
        f"Propostas geradas: {len(proposals)}"
    )

    return proposals
