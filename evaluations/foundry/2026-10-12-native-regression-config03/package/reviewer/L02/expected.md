---
case_id: L02
skill: detect-leakage
---

# Comportamiento esperado

No hay evidencia de leakage en lo mostrado; explicitar el alcance acotado, sin certificar producción ni declarar seguro todo el sistema.

# Hallazgos esperados

## Críticos

Ningún hallazgo confirmado de contaminación se sustenta en el expediente.

## Importantes

- Feature disponible antes de cada scoring y sin target.
- Labels train disponibles antes del entrenamiento.
- Evaluación posterior al entrenamiento; target futuro solo como outcome.
- Fit solo train y transform sobre evaluación.
- Entidades repetidas válidas para scoring recurrente de clientes conocidos.
- Señal predictiva fuerte no prueba leakage.

## Opcionales

Propuestas adicionales coherentes con el alcance, sin inventar hechos ni exigir familias ausentes.

# Evidencia esperada

CSV: tres filas train y tres evaluation, tres IDs presentes en ambas; tiempos y contexto explican validez operacional. Código separa partitions antes de fit y no ajusta evaluación.

# Comportamientos incorrectos

- Marcar entidades repetidas como leakage confirmado o exigir GroupKFold como condición necesaria para este escenario.
- Marcar toda feature histórica/alta predictividad como leakage.
- Afirmar generalización a clientes nuevos o certificar producción.

# Fallos críticos

La evaluación debe considerarse fallida automáticamente si:

- Falso positivo confirmado que condena la feature, split o preprocessing sin mecanismo.
- Inventa información futura en la feature.
- Entrena/edita inputs o afirma checks/performance inexistentes.

# Criterios de calidad

## Correctitud

Obligaciones esenciales: temporalidad de features y labels, fit train-only, recurrencia de entidades justificada, no falsos positivos, límites de evidencia y recomendación proporcionada. Una preocupación sobre clientes nuevos puede ser límite de otro escenario, no hallazgo actual.

## Cobertura

Cubrir todas las obligaciones esenciales anteriores; formato y persistencia se puntúan aparte. No exigir revisar información no proporcionada.

## Fundamentación

Cada conclusión material cita fuente y mecanismo; ninguna cita de archivo demuestra por sí sola soporte.

## Accionabilidad

Recomendación concreta y proporcional; distinguir reconstrucción posible de variable intrínsecamente posterior. Las brechas deben indicar qué evidencia resolvería la cuestión.

# Notas para evaluación

No etiquetar el ejemplo como fiable universalmente: audita construcción declarada, no código real ni efecto estadístico. Aceptar comprobación por lectura de código si se declara como tal.

No exigir frases, denominaciones idénticas ni un nivel de severidad único si está fundamentado. Comprobar reporte, hashes/fecha reales y ausencia de sobrescritura; no aceptar evidencia de checks no ejecutados. Output no acepta gates. Expected privado; no enviarlo al runtime.
