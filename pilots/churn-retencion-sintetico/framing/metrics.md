# Métricas del piloto

## Definiciones aprobadas en discovery

K=50 contactos por mes; unidad cliente activo al inicio del mes. Si un mes tiene menos de 50 clientes, la política selecciona min(50, N); debe reportar el K efectivo.

- Precision@K: positivos seleccionados / K efectivo.
- Recall@K: positivos seleccionados / positivos observados del mes. Si no hay positivos, registrar no definido; no forzar cero o uno.
- Lift@K (complementaria propuesta): Precision@K / prevalencia observada del mes; no definido con prevalencia cero.

Reportar meses individualmente y media entre meses evaluables. Pending nunca es negativo ni entra en el denominador de una métrica supervisada. Enero de 2026 se reserva para scoring sin evaluación en esta extracción.

La referencia aleatoria esperada de Precision@K es la prevalencia del mismo mes, no el 4,08% global aplicado indistintamente. Una regla simple servirá como baseline analítico, con parámetros fijados usando desarrollo.

MRR en riesgo resume precios ficticios de clientes que cancelan. No demuestra que una campaña evite churn ni estima margen recuperable.

## Aceptación del trabajo

Para continuar con análisis se requiere contrato framing revisado, diccionario/checks trazables y diseño de validación revisado. El primer análisis debe ser reproducible y respetar ventanas y splits; si no supera el baseline, reportarlo sin cambiar el test para mejorar resultados.

No se fija un umbral comercial arbitrario ni una mejora de ROI. La performance predictiva sigue desconocida.
