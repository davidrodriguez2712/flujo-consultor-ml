# Fragmento auditable; no ejecutar ni entrenar.
FEATURE_COLUMNS = ["history_kwh_90d", "recovered_kwh"]
def build_features(rows):
    return [{name: row[name] for name in FEATURE_COLUMNS} for row in rows]
