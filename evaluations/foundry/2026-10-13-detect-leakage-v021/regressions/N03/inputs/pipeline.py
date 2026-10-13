# Orden declarado; no ejecutar.
def prepare(data, scaler):
    normalized = scaler.fit_transform(data[["amount"]])
    train = normalized[data["partition"] == "train"]
    evaluation = normalized[data["partition"] == "evaluation"]
    return train, evaluation
