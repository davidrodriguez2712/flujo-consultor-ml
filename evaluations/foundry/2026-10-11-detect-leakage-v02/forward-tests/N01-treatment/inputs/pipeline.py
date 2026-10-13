# Fragmento para inspección; no ejecutar.
FEATURE_COLUMNS = ["payment_sum_previous_day"]
def features(rows):
    return rows[FEATURE_COLUMNS]
