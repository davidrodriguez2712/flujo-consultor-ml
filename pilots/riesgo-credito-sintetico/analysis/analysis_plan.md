# Plan de análisis — Execution de development

## Inputs

Cinco CSV congelados y contrato/diseño de Diagnosis aprobado. El loader de development solo interpreta labels de train disponibles al2025-01-01 y validation enero–febrero disponibles al2025-06-15. El raw del periodo final no está oculto; se prohíbe usar sus métricas para configurar modelos.

## Procedimiento

1. Confirmar hash de código, policy e inputs contra freeze previo.
2. Leer applications/history/outcomes y validar claves1:1; sin join por cliente ni incorporación de decisiones/columnas posteriores.
3. Fit del baseline y referencia solo en train, predict validation sin modificar transformaciones.
4. Calcular Brier/ROC-AUC/calibración, comparar sobre mismas filas y Top-K mensual retrospectivo de concedidas maduras.
5. Conservar modelo, scores, referencia, resultados, policy y summary en directorio nuevo; no sobrescribir.
6. Revisar contenido de Execution y después preparar refit/evaluación final con protocolo congelado. No ejecutar final hasta aprobar este gate.

## QA

Tests de guards temporales, NaN, aislamiento de IDs/outcomes, transformaciones de train, métricas con expected aritméticos, empates, missinglabels, loader filtrado y freeze. Revisión por otro agente antes del freeze, sin aprobar gates humanos. No confundir proceso correcto con beneficio causal o eficacia de las skills.
