def suggest_adjustment(evaluation):
    trend = evaluation.get("trend")
    score = evaluation.get("score", 0)

    if trend == "improved":
        return {
            "action": "maintain",
            "reason": "O resultado atual superou a média anterior."
        }

    if trend == "declined":
        return {
            "action": "review",
            "reason": "O resultado atual ficou abaixo da média anterior."
        }

    if trend == "stable":
        return {
            "action": "experiment",
            "reason": "O resultado permaneceu estável; testar uma variação pode gerar informação nova."
        }

    return {
        "action": "establish_baseline",
        "reason": f"Primeira referência estabelecida com score {score}."
    }
