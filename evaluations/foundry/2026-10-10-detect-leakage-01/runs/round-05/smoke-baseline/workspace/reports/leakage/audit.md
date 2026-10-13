# Auditoría smoke técnico: inputs (sin evaluación de leakage)

Fecha: 2026-10-11
Tipo: smoke técnico. No cuenta como evidencia de eficacia.

## 1. Alcance y autoridad

- Leídos: `workflow.md`, `case.md`, `.runtime/check_inputs.py`, `inputs/data.csv`.
- Ejecutado: únicamente la utility fija autorizada (`check_inputs.py`), sin argumentos.
- Según `case.md`: no se evaluó leakage, no se entrenó ningún modelo y no se modificó ningún input.
- Skill `acos-eval:detect-leakage`: **none/null**. No figuraba entre las skills disponibles en este entorno, por lo que no se invocó y la tarea se realizó sin ella.
- No se usaron subagentes, red, instalación de paquetes ni comandos adicionales.

## 2. Hechos observados (salida de la utility)

| Ruta | SHA-256 | Bytes | Columnas | Filas |
|---|---|---|---|---|
| `case.md` | `c55d6e5472cc2697b8c2c491ec1786ee9acd2e0cae2d311c691fea646a51e232` | 290 | — | — |
| `inputs/data.csv` | `8028f83b208c1c7608522c1680cb03dfeaf3a79fa2224fd257d7e31be883dbab` | 21 | `entity_id`, `value` | 1 |

Contenido leído de `inputs/data.csv` (dos líneas): cabecera `entity_id,value` y una fila `s1,1`.

## 3. Verificaciones deterministas

- La utility se ejecutó una vez, con el comando exacto autorizado, y devolvió JSON válido con los dos archivos listados.
- Conteo de filas de `data.csv`: 1, coincidente con la lectura directa.
- Hashes y tamaños reportados por la utility; no se recalcularon por otro medio.
- No se detectaron errores de ruta ni symlinks en la salida.

## 4. Inferencias y limitaciones

- Con una sola fila, el archivo no permite evaluar leakage (ni de target, ni temporal, ni de agregación); cualquier conclusión sobre fuga sería un supuesto, no un hecho. Por eso no se emite ninguna.
- No hay columna de target, fecha, ni definición de población o unidad en el expediente. Son brechas de datos y definición que impedirían una auditoría de leakage real aun con más filas.
- `case.md` indica que el smoke no cuenta como eficacia; este reporte tampoco.
- No se verificó la procedencia de `inputs/data.csv` más allá de su hash.

## 5. Paradas y escalamiento (workflow)

- Se detecta **datos insuficientes** para la verificación de leakage que el encargo real requeriría. Según `workflow.md`, esto corresponde a parar o pedir decisión humana, no a rellenar la brecha con supuestos.
- Opciones seguras: (a) aceptar este resultado como smoke técnico de lectura y hash; (b) aportar un dataset con target, variables candidatas, fechas y definición de unidad/población, con un owner que acepte dichas definiciones, antes de cualquier auditoría de leakage.
- No se tomó ninguna decisión de negocio ni de promoción.

## 6. Recomendación

Cerrar este run como smoke técnico completado (lectura, hash y conteo verificados). Para una auditoría de leakage sustantiva, requerir un expediente con datos suficientes y un owner de definiciones.

## 7. Checks

- Formato del reporte: secciones 1–7 presentes, separación entre hechos, verificaciones, inferencias y recomendaciones.
- Contenido: verificaciones deterministas representadas tal como salieron; ningún resultado de leakage afirmado.
