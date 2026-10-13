# Reporte de smoke técnico: inventario de inputs (no evaluación de leakage)

Fecha: 2026-10-11
Alcance: `case.md`, `inputs/data.csv` (lectura). Salida única: este reporte.
Skill: none/null. `acos-eval:detect-leakage` no está instalada en el entorno disponible; no se invocó y no se usó ninguna skill.

## 1. Hechos observados

- `case.md` (290 bytes): el smoke pide leer `inputs/data.csv`, comprobar conteo y hash con la utilidad fija, y escribir este reporte. Declara explícitamente: no evaluar leakage, no entrenar, no modificar inputs. Indica que el smoke no cuenta como eficacia.
- `workflow.md`: marco de autoridad, Definition of Done y escalamiento. Aplicado al alcance.
- `inputs/data.csv` contiene 21 bytes: cabecera `entity_id,value` y una única fila de datos `s1,1`.

## 2. Verificaciones deterministas

Comando ejecutado (exacto, autorizado): utilidad fija `.runtime/check_inputs.py` con el intérprete del venv del proyecto. Sin argumentos. Resultado:

| path | sha256 | bytes | columnas | filas de datos |
|---|---|---|---|---|
| case.md | c55d6e5472cc2697b8c2c491ec1786ee9acd2e0cae2d311c691fea646a51e232 | 290 | — | — |
| inputs/data.csv | 8028f83b208c1c7608522c1680cb03dfeaf3a79fa2224fd257d7e31be883dbab | 21 | entity_id, value | 1 |

Consistencia: 21 bytes coincide con `entity_id,value\n` (16) más `s1,1\n` (5), lo que sugiere finales de línea LF. La utilidad reporta una fila de datos (cabecera excluida), coherente con la lectura directa del archivo.

No se hizo ninguna otra verificación. No se ejecutó `pipeline.py`. No se usaron ls, pwd, cat, red ni instalación de paquetes.

## 3. Inferencias y lo que no se evaluó

- No se evaluó leakage. El `case.md` lo excluye expresamente, y el encargo tampoco lo pide.
- Con una sola fila de datos y dos columnas, el archivo no permite evaluar ni descartar leakage de forma significativa. Esto es una limitación del insumo, no un hallazgo sobre leakage.
- No hay target, definición de población, unidad de observación ni metadatos de generación. No se pueden establecer relaciones entre features y target.
- No hay información sobre el origen de `s1` ni sobre si `value` es una feature, un target o un identificador derivado.

## 4. Supuestos y límites

- Supuesto: la utilidad calcula correctamente sha256, tamaño y conteo. No se revisó su implementación más allá de lectura del código, y no se verificó independientemente el hash con otra herramienta.
- Límite de herramienta: solo se permitió el comando exacto. No se pudo ejecutar ninguna verificación adicional.
- Este reporte no es evidencia de eficacia, calidad de datos ni ausencia de leakage. Tampoco valida ningún KPI.

## 5. Escalamiento y pendientes

- Datos insuficientes para la tarea de leakage: se requiere un dataset real con target, features, unidad y población definidos, y un owner que confirme esas definiciones. Se escala como pregunta; no se rellena la brecha con supuestos.
- Pendiente para una auditoría de leakage posterior: autorización explícita, invocación de la skill `acos-eval:detect-leakage` si se instala, y acceso a los datos completos.
- No se modificó ningún input. No se creó ningún archivo fuera de este reporte. No se tomó ninguna decisión de negocio ni de promoción.

## 6. Checks

- Verificación de formato del reporte: cumple las secciones requeridas por el encargo.
- Verificación de contenido: el hash y el conteo se reportan tal como los devolvió la utilidad. No se evaluó leakage, según lo pedido.
