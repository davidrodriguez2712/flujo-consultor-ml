# Aceptación propuesta — pendiente de aprobación

## Corrección y reproducibilidad

Antes de modelar, aprobar definición de target, población, disponibilidad, features admisibles, reglas de split, métricas y política de ranking. Conservar código, configuración, seeds, hashes y resultados. No completar labels pendientes/rechazadas ni usar variables posteriores, target, decisiones de concesión o IDs como predictors. Un join por cliente no debe multiplicar solicitudes.

Separar evidencia sobre clientes recurrentes y clientes nuevos cuando el diseño temporal lo permita; no forzar un group split sin comprobar qué uso representa. Las conclusiones que no tengan muestra o ambas clases se registran como no determinables.

## Desempeño técnico

Comparar Brier del baseline frente al predictor constante fit en train, en las mismas filas del holdout congelado. Diferencia positiva de Brier(referencia)-Brier(modelo) permite decir «mejora puntual observada en este fixture»; diferencia cero/negativa obliga a reportar ausencia de mejora. No constituye evidencia suficiente de generalización real o eficacia de las skills.

Informar ROC-AUC y calibración aunque sean desfavorables; no seleccionar modelo, bins o thresholds después de observar holdout. No se fija un ROC-AUC arbitrario como criterio de éxito de negocio. La ejecución puede ser correcta y el modelo no útil: separar esos resultados.

## Decisión y selección

Hasta 100 revisiones/mes, ranking descendente de riesgo con empate por application_id ascendente. Declarar periodo, población elegible, K efectivo, exclusiones y coverage. La evaluación offline usa exclusivamente concedidas maduras; el ranking sobre todas las solicitudes no tiene métricas globales identificadas si incluye rechazadas o pendientes. No reemplazar labels ausentes por cero.

No aprobar crédito ni afirmar ahorro, beneficio incremental o causalidad de la revisión. Una propuesta puede recomendar no usar el modelo o recopilar información adicional.

## Gates

Cada etapa requiere checks y revisión humana del contenido. PASS de Discovery no aprueba Framing, diagnóstico, modelado ni uso real. La aprobación de Framing permitirá elaborar Diagnosis y el diseño de validación; el entrenamiento espera los gates previos pertinentes.
