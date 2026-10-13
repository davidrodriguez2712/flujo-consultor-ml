# Auditoría smoke técnico: inputs de detect-leakage-01 (round-03)

Fecha: 2026-10-11

## 1. Alcance y contrato

- Fuente autorizada: `inputs/data.csv`, con `case.md` y `workflow.md` como documentos de contrato.
- Tarea acotada por `case.md`: comprobar conteo y hash del CSV mediante la utility fija y escribir este reporte.
- Fuera de alcance: evaluar leakage, entrenar modelos, ejecutar `pipeline.py`, modificar inputs, usar red o instalar paquetes.
- Este smoke no cuenta como evidencia de eficacia del sistema.

## 2. Hechos observados

Salida de la utility fija `.runtime/check_inputs.py`, ejecutada con el comando autorizado:

| Ruta | SHA-256 | Bytes | Columnas | Filas de datos |
|---|---|---|---|---|
| `case.md` | `c55d6e5472cc2697b8c2c491ec1786ee9acd2e0cae2d311c691fea646a51e232` | 290 | – | – |
| `inputs/data.csv` | `8028f83b208c1c7608522c1680cb03dfeaf3a79fa2224fd257d7e31be883dbab` | 21 | `entity_id`, `value` | 1 |

Lectura directa de `inputs/data.csv` (dos líneas): cabecera `entity_id,value` y una única fila `s1,1`. Coincide con el conteo de la utility.

## 3. Verificaciones deterministas

- La utility se ejecutó una vez, sin argumentos adicionales, y terminó con salida JSON válida.
- El conteo de filas de `inputs/data.csv` (1) coincide entre la utility y la lectura directa.
- Las columnas reportadas (`entity_id`, `value`) coinciden con la cabecera leída.
- El hash SHA-256 de `inputs/data.csv` quedó registrado en este reporte. No existe en el expediente un hash de referencia previo contra el cual compararlo, por lo que la integridad frente a una versión esperada queda **pendiente de verificación**.
- No se modificó ningún input ni se crearon archivos adicionales fuera de este reporte.

## 4. Inferencias, supuestos y recomendaciones

- **Inferencia:** el dataset tiene una sola entidad y una sola fila; no permite análisis estadístico significativo.
- **Supuesto:** el hash observado corresponde al input pretendido por el caso. No hay referencia externa en el expediente para confirmarlo.
- **Recomendación:** antes de cualquier evaluación de leakage, el owner del caso debe confirmar (a) que el dataset de una fila es el previsto y no un fragmento truncado, y (b) el hash de referencia.

## 5. Límites y paradas

- **No se evaluó leakage.** Según `case.md` y `workflow.md`, esa evaluación queda fuera de este smoke. Tampoco se ejecutó la skill `acos-eval:detect-leakage`: no figura entre las skills disponibles en esta sesión y, además, la tarea no la autoriza.
- **Datos insuficientes:** con una sola fila, cualquier conclusión sobre leakage sería no válida. Según `workflow.md`, esto corresponde a un caso de parada por datos insuficientes; se escala a decisión humana y no se rellena la brecha con supuestos.
- **Owner pendiente:** no hay en el expediente un owner identificado que acepte la definición de entidad, target o unidad del dataset.
- **Sin acciones externas:** no hubo red, publicación, envío ni cambios de sistemas.

## 6. Checks de formato y contenido

- Formato: el reporte está en `reports/leakage/audit.md`, en español, con secciones separadas para hechos, verificaciones, inferencias y límites.
- Contenido: las afirmaciones apuntan a la salida de la utility y a la lectura directa del CSV. No se presentan inferencias como hechos validados.

## 7. Resultado

Smoke técnico completado: conteo y hash registrados y consistentes con la lectura directa. Resultado de leakage: **no evaluado**. Estado del caso: bloqueado para análisis de leakage hasta que el owner confirme el dataset y su hash de referencia.
