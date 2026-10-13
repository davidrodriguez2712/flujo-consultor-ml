# Model brief

Objetivo: ranking mensual de clientes identificables por ventas válidas siguientes90d. Ocho features fijadas en plan; targets maduros, expanding window y cuatro development. Baseline ventas90; RFM ordinal informativo (MAE monetario no aplica). Ridge log con scaler train; única alternativa HistGradient log con configuración fija. Seed20261009, sin tuning. Detalles/hashes: validation/evaluation_contract.yaml, reports/execution/model_runs.json.

Ningún modelo supera baseline en development. Holdout reservado. No inferir uplift, CLV completo, margen o readiness comercial.
