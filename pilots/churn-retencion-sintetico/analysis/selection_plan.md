# Plan de selección — revisión de validation

## Regla ejecutada

Población: clientes activos al primer día de cada mes. Unidad: cliente-mes. Capacidad aprobada: 50/mes. Ordenar score de riesgo descendente y customer_id ascendente para empates. K efectivo es min(50, población); en todos los seis meses es 50. No ajustar por outcomes, MRR o feedback del test.

## Evidencia

Modelo único congelado al 1 de julio de 2025. Scores y selected_ids por mes en analysis/outputs/holdout-final. 300 selecciones cliente-mes, 32 positivos; no asumir clientes distintos ni contactos realizados. Auditoría recalcula orden y métricas. Precision media 10,67%, Recall 11,02%, Lift 2,52.

## Límites operativos

Esta regla prioriza riesgo, no beneficio causal de una intervención. No incorpora consentimiento, contactabilidad, supresión de contactos recientes, costes, fairness ni optimización comercial. Si se añaden restricciones debe revisarse otro protocolo; no modificar la regla para mejorar retrospectivamente el test. MRR es descriptivo, no ROI. No hay campañas ejecutadas. Gate selection-review pendiente.
