# Model brief — baseline de development

## Objetivo

Estimar riesgo de 30DPD dentro de 90 días en créditos concedidos, con información al scoring. Priorizar revisión de solicitudes es una propuesta de laboratorio; esta fase no evalúa una política causal ni generaliza a rechazadas.

## Baseline y referencia

Regresión logística L2 con cinco features admisibles: monthly_income, debt_to_income, requested_amount, bureau_score, prior_late_count. Imputación por mediana, mean y escala poblacional fit solo en train; escala1 si es constante. Gradient descent full-batch,600iteraciones, learning_rate0.05, L2=0.01. Intercepto inicial logit de prevalencia de train, sin penalizar. No búsqueda de hiperparámetros, selección de features ni resampling. La loss es binary log loss media +0.5*L2*suma(peso²). El sigmoid usa saturación numérica en[-35,35].

Referencia: probabilidad constante igual a positivos/filas de train; ambas evaluadas sobre idénticas solicitudes concedidas y maduras. IDs, outcome y columnas de decisión/posteriores no entran como features. Transformaciones permanecen fijas al predecir.

## Diseño temporal aprobado

Fit de development al2025-01-01:1.248 filas,134positivos. Validation scoring enero–febrero2025, labels disponibles al2025-06-15:298filas. No evaluar julio–septiembre todavía. Ver `validation/validation_design.yaml` y diseño aprobado con la revisión de Diagnosis.

## Resultados y autoridad

Comparar Brier, ROC-AUC, bins de calibración prefijados y Top-K mensual retrospectivo de concedidas. No seleccionar nuevas configuraciones a partir de holdout. Resultado desfavorable también se conserva. Execution requiere revisión humana antes del finalfit/holdout. No hay aprobación de uso real por una métrica favorable.

## Implementación

`analysis/credit_baseline.py`, pruebas `analysis/test_credit_baseline.py`, policy en `reports/execution/implementation-policy.yaml`. Se congelarán hashes de código, configuración e inputs antes de ejecutarlos contra datos reales del fixture. Las pruebas del runner usan copias generadas en tmp_path; sus métricas no se usaron para elegir configuración.
