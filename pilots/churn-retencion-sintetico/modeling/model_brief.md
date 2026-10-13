# Baseline de churn — especificación previa a métricas

## Decisión y alcance

Priorizar 50 clientes activos cada mes. Estimar riesgo de cancelación durante el mes del scoring. Datos sintéticos; no predecir beneficio causal de una campaña.

## Método fijado

Estimación de frecuencia por grupos definidos por actividad missing, caída de actividad de al menos 50% respecto del mes anterior, presencia de pagos fallidos y presencia de tickets. Hasta 16 grupos. Suavizado: 20 pseudoobservaciones con prevalencia del train; grupo nuevo usa dicha prevalencia. Imputación de actividad con mediana aprendida únicamente en train.

Es una referencia interpretable, sin ajuste de hiperparámetros. El umbral 50% y suavizado 20 son elecciones de trabajo fijadas antes de ejecutar métricas, no óptimos demostrados. No se utilizan los coeficientes internos del generador.

## Datos permitidos

Solo active_days_prev_month, active_days_prev2_month, failed_payments_prev_month y support_tickets_prev_month. Customer ID sirve para unir y desempatar, no para estimar riesgo. MRR solo describe importes de positivos seleccionados; no es predictor ni recupero.

## Validación y outputs

Nueve folds septiembre 2024–mayo 2025. Train histórico con labels disponibles al inicio del fold. Precision@50, Recall@50 y Lift@50 mensual, frente a expectativa analítica de selección aleatoria del mismo mes. Medias macro por mes; no una prueba de significancia.

Congelar modelo final con train disponible al 1 de julio 2025, hasta snapshots de mayo. No evaluar julio–diciembre todavía. Código: analysis/baseline.py. Policy y modelos: analysis/outputs/baseline-development/. Revisión humana del gate execution pendiente.
