def suggest_adjustment(evaluation):
    trend = evaluation.get("trend")
    score = float(evaluation.get("score", 0.0))

    history = evaluation.get("history", {})
    historical_trend = history.get("trend")
    historical_average = history.get("average")
    historical_samples = history.get("samples", 0)

    # A avaliação atual continua sendo a referência principal.
    # O histórico apenas adiciona contexto à adaptação.
    if trend == "improved":
        action = "maintain"
        reason = "O resultado atual superou a média anterior."

    elif trend == "declined":
        action = "review"
        reason = "O resultado atual ficou abaixo da média anterior."

    elif trend == "stable":
        action = "experiment"
        reason = (
            "O resultado permaneceu estável; "
            "testar uma variação pode gerar informação nova."
        )

    else:
        action = "establish_baseline"
        reason = (
            f"Primeira referência estabelecida com score {score}."
        )

    # Contexto histórico adicional.
    if historical_trend is not None:
        reason += (
            f" Tendência histórica: {historical_trend}."
        )

    if historical_average is not None:
        reason += (
            f" Média histórica: "
            f"{float(historical_average):.4f}."
        )

    return {
        "action": action,
        "reason": reason,
        "score": score,
        "trend": trend,
        "history": {
            "trend": historical_trend,
            "average": historical_average,
            "samples": historical_samples,
        },
    }
