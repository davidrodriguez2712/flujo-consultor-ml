# Auditoría de smoke técnico: detect-leakage

## Alcance

- Fuentes leídas: `workflow.md`, `case.md`, `inputs/data.csv` y `.runtime/check_inputs.py` (solo lectura).
- Utility ejecutada una vez, sin argumentos: `.runtime/check_inputs.py` (salida JSON con hashes, tamaños y conteos).
- No se ejecutó `pipeline.py`, no se evaluó leakage, no se entrenó ningún modelo y no se modificó ningún input.
- La skill `acos-eval:detect-leakage` no está disponible en el entorno (solo consta `plugin-authoring`), por lo que no fue invocada.

## Hechos observados

| Archivo | SHA-256 | Bytes | Columnas | Filas |
|---|---|---|---|---|
| `case.md` | `c55d6e5472cc2697b8c2c491ec1786ee9acd2e0cae2d311c691fea646a51e232` | 290 | — | — |
| `inputs/data.csv` | `8028f83b208c1c7608522c1680cb03dfeaf3a79fa2224fd257d7e31be883dbab` | 21 | `entity_id`, `value` | 1 |

Contenido de `inputs/data.csv` (leído directamente): encabezado `entity_id,value` y una única fila `s1,1`.

## Verificaciones deterministas

- Conteo de filas CSV: 1 (confirmado por la utility y por lectura directa).
- Columnas: `entity_id`, `value` (confirmado por ambas fuentes).
- Hashes y tamaños reportados por la utility para los dos archivos incluidos.

## Límites

- Este es un smoke técnico de inputs. **No cuenta como evidencia de eficacia** ni como evaluación de leakage.
- Con una sola fila no es posible evaluar leakage, distribución, cortes temporales, duplicados ni relación target–features.
- No hay columna target identificada ni artefacto de pipeline auditado; cualquier conclusión sobre leakage queda pendiente.
- Los hashes identifican bytes en el momento de la lectura; no validan semántica ni representatividad de los datos.

## Pendientes

- Dato pendiente → evaluación de leakage: se requiere un dataset con volumen suficiente, definición de target y fechas de corte, y la ejecución del procedimiento de leakage autorizado.
- Dato pendiente → reproducibilidad: no hay recorrido de pipeline ejecutado en este smoke.

## Conclusión

Se verificaron conteo (1 fila), columnas y hashes de `inputs/data.csv` y `case.md` mediante la utility fija. No se formula ningún juicio sobre leakage.
