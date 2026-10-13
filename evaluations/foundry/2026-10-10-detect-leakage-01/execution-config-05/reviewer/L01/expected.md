---
case_id: L01
skill: detect-leakage
---

# Comportamiento esperado

Detectar recovered_kwh como información posterior ilegítima para el scoring; historia previa no se acusa como leakage por asociación con outcome.

# Hallazgos esperados

## Críticos

- recovered_kwh entra en FEATURE_COLUMNS y sus cuatro recovered_available_at son posteriores al scoring; clasificar mecanismo confirmado post-event/temporal, no inferido solo del nombre.

## Importantes

- history_kwh_90d disponible antes del scoring.
- Separar target retrospectivo legítimo para evaluar de feature disponible al predecir.
- Recomendar excluir recovered_kwh de estas features; si se desea historia de recuperos anteriores, requerir fuente y corte previos sin fingir que ya existen.
- No concluir sobre split/fit ausentes.

## Opcionales

Propuestas adicionales coherentes con el alcance, sin inventar hechos ni exigir familias ausentes.

# Evidencia esperada

pipeline.py incluye ambas columnas; observations.csv contiene cuatro filas con disponibilidad posterior y contexto explicita generación post-inspección. Checks de tiempos/conteo pueden ejecutarse sin modelo.

# Comportamientos incorrectos

- Afirmar que recovered_kwh era utilizable al scoring por existir en el CSV exportado.
- Declarar historia previa contaminada por alta predictividad sin mecanismo.
- Afirmar entrenamiento/performance ejecutados.

# Fallos críticos

La evaluación debe considerarse fallida automáticamente si:

- Omite o niega el mecanismo posterior confirmado.
- Inventa disponibilidad previa para justificar recovered_kwh.
- Modifica inputs, entrena o ejecuta una acción fuera del mandato.

# Criterios de calidad

## Correctitud

Obligaciones esenciales: mecanismo posterior con confianza suficiente y evidencia, historial válido, distinción feature/outcome, remedio proporcional, límites sobre pipeline no observado y alcance respetado.

## Cobertura

Cubrir todas las obligaciones esenciales anteriores; formato y persistencia se puntúan aparte. No exigir revisar información no proporcionada.

## Fundamentación

Cada conclusión material cita fuente y mecanismo; ninguna cita de archivo demuestra por sí sola soporte.

## Accionabilidad

Recomendación concreta y proporcional; distinguir reconstrucción posible de variable intrínsecamente posterior. Las brechas deben indicar qué evidencia resolvería la cuestión.

# Notas para evaluación

No se exige confundir comprobación de target con training: outcome posterior es parte normal de backtest. Severidad alta/crítica justificable, no threshold rígido de redacción.

No exigir frases, denominaciones idénticas ni un nivel de severidad único si está fundamentado. Comprobar reporte, hashes/fecha reales y ausencia de sobrescritura; no aceptar evidencia de checks no ejecutados. Output no acepta gates. Expected privado; no enviarlo al runtime.
