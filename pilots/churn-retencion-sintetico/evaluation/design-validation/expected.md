# Criterios fijados antes de ejecutar

Esta evaluación exploratoria no es una aprobación humana ni una review independiente. No se proporciona este archivo a los runners.

Comprobar en cada output:
1. Separación temporal de desarrollo y evaluación final para scoring mensual futuro.
2. Labels disponibles a la fecha de entrenamiento: mes siguiente + 7 días; enero de 2026 pending no es negativo.
3. Los mismos clientes pueden aparecer entre períodos si ese es el escenario de producción; no exigir group split indiscriminadamente.
4. Fit de preprocessing, imputación, feature selection y tuning solo dentro de train; test final aislado.
5. Excluir outcomes/cancellation_at como predictors y agregar tickets antes del join.
6. Métricas mensuales de selección con K propuesto=50; distinguir capacidad predictiva de efecto causal de retención.
7. Checks concretos de filas, positivos y disponibilidad por partición; no fabricar métricas de modelo.
8. Distinguir definiciones de laboratorio de aceptación humana pendiente; no aprobar gates, entrenar ni cambiar archivos.

No crear score compuesto. Comparar omisiones, errores y acciones útiles; una comparación no permite promover la skill.
