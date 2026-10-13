# Orden declarado; no ejecutar.
def prepare(data, encoder, scaler):
    train = data[data["partition"] == "train"]
    evaluation = data[data["partition"] == "evaluation"]
    id_train = encoder.fit_transform(train[["client_code"]])
    id_eval = encoder.transform(evaluation[["client_code"]])
    x_train = scaler.fit_transform(train[["usage_previous_30d"]])
    x_eval = scaler.transform(evaluation[["usage_previous_30d"]])
    return id_train, id_eval, x_train, x_eval
