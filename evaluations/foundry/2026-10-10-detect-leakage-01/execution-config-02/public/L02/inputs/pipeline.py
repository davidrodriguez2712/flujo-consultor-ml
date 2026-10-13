# Orden declarado para inspección; no ejecutar/entrenar.
def prepare(data, scaler):
    train = data[data["partition"] == "train"]
    evaluation = data[data["partition"] == "evaluation"]
    feature_columns = ["usage_previous_30d"]
    x_train = scaler.fit_transform(train[feature_columns])
    x_evaluation = scaler.transform(evaluation[feature_columns])
    return x_train, x_evaluation
