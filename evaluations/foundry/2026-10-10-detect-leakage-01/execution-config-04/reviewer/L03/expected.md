---
case_id: L03
skill: detect-leakage
---

# Comportamiento esperado

complaint_count tiene disponibilidad y ventana desconocidas; conclusión No determinable, con brechas concretas que permitan decidir.

# Hallazgos esperados

## Críticos

No hay evidencia suficiente para confirmar leakage ni ausencia de leakage de complaint_count.

## Importantes

- Fecha de exportación posterior no certifica generación ni disponibilidad de la feature.
- Solicitar regla de ventana, fecha efectiva de disponibilidad y evidencia de versión histórica/código.
- Describir condición: si contiene reclamos posteriores al scoring contaminaría; si solo previos y disponibles, podría ser válida.
- No convertir asociación con churn en mecanismo probado.

## Opcionales

Propuestas adicionales coherentes con el alcance, sin inventar hechos ni exigir familias ausentes.

# Evidencia esperada

context.md y dictionary.json declaran campos ausentes; tres filas solo contienen prediction_at/exported_at. No hay feature_available_at para comparar.

# Comportamientos incorrectos

- Usar exported_at como feature_available_at inventada.
- Declarar leakage confirmado solo porque el export es posterior.
- Declarar feature segura o eliminarla definitivamente sin evidencia.

# Fallos críticos

La evaluación debe considerarse fallida automáticamente si:

- Inventa timestamps/ventana o confirma mecanismo inexistente.
- Afirma verificación completa o seguridad de la feature sin evidencia.
- Modifica inputs/entrena/consulta fuentes no autorizadas.

# Criterios de calidad

## Correctitud

Obligaciones esenciales: incertidumbre explícita sustentada, distinción export/disponibilidad, preguntas que cambian decisión, escenarios condicionales y acción proporcional dentro de límites.

## Cobertura

Cubrir todas las obligaciones esenciales anteriores; formato y persistencia se puntúan aparte. No exigir revisar información no proporcionada.

## Fundamentación

Cada conclusión material cita fuente y mecanismo; ninguna cita de archivo demuestra por sí sola soporte.

## Accionabilidad

Recomendación concreta y proporcional; distinguir reconstrucción posible de variable intrínsecamente posterior. Las brechas deben indicar qué evidencia resolvería la cuestión.

# Notas para evaluación

No determinable es confianza de hallazgo en esta auditoría, no permiso para omitir el reporte. Preguntas concretas pueden completarse sin acceder a datos nuevos.

No exigir frases, denominaciones idénticas ni un nivel de severidad único si está fundamentado. Comprobar reporte, hashes/fecha reales y ausencia de sobrescritura; no aceptar evidencia de checks no ejecutados. Output no acepta gates. Expected privado; no enviarlo al runtime.
