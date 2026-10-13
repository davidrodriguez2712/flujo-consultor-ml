# Plan de evaluación final

## Contexto aprobado

Execution de development aprobada por David. Se conserva algoritmo/configuración, features, bins y capacidad. El baseline y artefactos de development no se editan. Diseño temporal aprobado en Diagnosis: refit al 2025-07-01, scoring julio–septiembre y evaluación al 2026-01-15.

## Procedimiento

1. Verificar hashes de runner nuevo, baseline intacto, policy e inputs contra freeze.
2. Train: scoring anterior al cutoff y label observed disponible <= cutoff, antes de interpretar target; refit único de transformaciones/modelo/referencia.
3. Load scoring: applications/history por application_id 1:1, fechas disponibles, sin leer outcomes/decisiones/post_decision como features.
4. Score todas las solicitudes del periodo con un modelo fijo y persistir predicciones/modelo/referencia en staging.
5. Leer labels de esas solicitudes, aplicando disponibilidad al timestamp de evaluación; mantener rechazadas/pendientes sin target.
6. Evaluar Brier/ROC-AUC/calibración y cortes por mes/nuevos/recurrentes solo en concedidas maduras. Reportar ranking de esa población por separado del Top-K de todas las solicitudes.
7. Para todas las solicitudes: IDs, elegibles, K y cobertura; Recall/Lift requieren población completamente etiquetada y Precision todos los seleccionados etiquetados. Los ausentes no son0.
8. Finalizar outputs con rename del directorio completo, sin sobrescribir. Auditoría posterior independiente y revisión humana de los cinco gates de Validation.

## Límites

No tuning, reentrenamiento mensual, aprobación crediticia, causalidad ni ahorro. Conocido/nuevo se define respecto de clientes del train admisible, no de toda la historia. Top-K mensual retrospectivo no es política online previa al desembolso. La comparación será puntual: no se plantea inferencia de significancia ni CI que asuma independencia de solicitudes.
