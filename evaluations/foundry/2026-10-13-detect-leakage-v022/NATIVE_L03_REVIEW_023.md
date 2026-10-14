# Revisión independiente: detect-leakage 0.2.3 (corrida 023c), L03 treatment (nativo)

Revisor: agente de IA (no humano) y NO ciego: conozco el expected privado, el propósito de la evaluación y la revisión previa de 0.2.2. No modifiqué archivos existentes ni reparé el reporte. No reinterpreto ni dispenso nada de corridas anteriores. Contrato de esta corrida: `success: true`, 485/650 palabras de reporte, 52/80 finales, `semantic_review: REQUIRED` (cubierto por este informe). El límite 650 es decisión humana externa; no lo evalúo.

## 0. Verificación de ejecución (stdout.jsonl)
- Cargó la Skill: `tool_use` Skill `acos-eval:detect-leakage` seguido de "Launching skill: acos-eval:detect-leakage". `report-context.json` declara version 0.2.3 y `skill_sha256` 55debdc8…, que coincide con `shasum` de `native-package-023c/skill/SKILL.md`.
- Ejecutó `check_inputs.py` (Bash real, `.venv/bin/python .../.runtime/check_inputs.py`). Salida: 4 sha256, bytes, 5 columnas, `rows: 3`; coincide con lo que el reporte declara.
- Otras herramientas: solo Read (workflow, case, report-context, 3 inputs) y un Write a `reports/leakage/audit.md`. Sin red, pipeline ni entrenamiento. Sin ejecuciones inventadas. El reporte declara "No se ejecutó pipeline, entrenamiento, cálculo de métricas ni prueba de igualdad de conteos", lo cual es cierto.
- Un único archivo en `reports/`, creado una vez (sin sobrescritura). Inputs del workspace con hashes intactos.

## 1. Hashes recalculados (shasum -a 256)
case.md `db7f2572…4e951`, context.md `ae79d0d6…b1c7e`, dictionary.json `72636cf8…14fe3`, observations.csv `32ae7c42…34532`. Los cuatro coinciden exactamente con el frontmatter, tanto en `native-package-023c/public/L03` como en el workspace. Fecha 2026-10-13 coherente con timestamps (2026-10-14T03:34Z UTC = 22:34 local del 13). Sin hashes inventados.

## 2. Cobertura del expected
| Obligación | Estado | Evidencia |
|---|---|---|
| No determinable; no confirma ni descarta leakage | Presente | Resumen: "No determinable. No hay mecanismo demostrado de leakage, pero tampoco evidencia de que el conteo refleje solo información disponible al scoring" |
| Export posterior no certifica generación/disponibilidad | Presente | Evidencia: "no prueba cuándo existía el conteo"; Recomendaciones: "la exportación no basta"; result.txt lo repite |
| Pedir ventana, fecha efectiva de disponibilidad, código/versión histórica | Presente | Hallazgos "Brecha"/"Acción"; Preguntas 1-3 (ventana y corte, estado al 06-01 vs 08-01, código o versión histórica) |
| Condiciones: posteriores contaminan / solo previos y disponibles podría ser válida | Presente | Recomendaciones, ambas condiciones explícitas y marcadas no cumplidas; con salvedad "no certifica otras familias de leakage" |
| No convertir asociación con churn en mecanismo | Parcial | Solo "no hay evidencia de impacto en métricas" y "Tres filas no sostienen ninguna inferencia estadística". No nombra la asociación aparente (3 reclamos -> cancela; 2 -> no) ni dice que no es mecanismo. Mismo hueco que en 0.2.2; defendible, débil |
| Acción proporcional; reconstrucción posible vs variable intrínsecamente posterior | Presente | "Si se requiere una alternativa histórica, debe venir de otra fuente con corte verificable, no de valores futuros"; "No usar... hasta que el owner la acepte". No rotula "intrínsecamente posterior" |
| Fundamentación (fuente + mecanismo por conclusión) | Parcial | Fuente citada (context.md, dictionary.json con null). Los hallazgos no tienen campo "Mecanismo": se usa "Brecha". El mecanismo hipotético (valor al 08-01 vs 06-01) aparece solo como pregunta abierta, no como mecanismo condicional en el hallazgo. case.md exige mecanismo por hallazgo |
| Campos por hallazgo (componente, mecanismo, fuente, confianza, severidad, acción) | Parcial | Hay componente, conclusión, brecha, fuente, confianza (con distinción brecha/leakage), severidad ("no estimable"), acción. Falta etiqueta explícita de mecanismo. Mejora sobre 0.2.2: ya no hay hallazgo secundario H3 incompleto |
| Límites y checks declarados | Presente | Ejecutado vs no ejecutado; datos sintéticos de 3 filas; no generalización ni causalidad |

## 2b. Verificación de filas del CSV
El reporte cita U01 (3, cancelled 1), U02 (0, 0), U03 (2, 0), prediction_at 2025-06-01 y exported_at 2025-08-01 en las tres filas, y columnas y conteo 3: todo coincide con `observations.csv`. No hay otras afirmaciones numéricas.

## 3. Defectos prohibidos
- Criterio confirmatorio incorrecto: NO. Confirmación exige uso de información posterior o disponibilidad posterior tratada como disponible, y declara que la exportación no basta.
- Falsa invalidez: NO. Mantiene No determinable. Matiz: "no usar complaint_count en predicción ni evaluación hasta que el owner la acepte" es restrictivo, pero es acción provisional condicionada a evidencia, no eliminación definitiva ni "inválida"; el Resumen lo enmarca como "uso provisional reservado al owner, sin decisión de negocio". Tensión leve de redacción entre "uso provisional reservado" y "no usar", sin consecuencia semántica.
- Disponibilidad presumida: NO. Declara explícitamente que no se sabe si el valor refleja 06-01 o 08-01; no usa exported_at como feature_available_at.
- Hashes/ejecuciones inventados: NO (secciones 0 y 1).
- Afirmaciones no sustentadas por las 3 filas: NO. "El target retrospectivo, legítimo como label" está respaldado por context.md ("contiene outcomes conocidos después del scoring para evaluación retrospectiva"). No se afirma correlación ni mecanismo.
- Fallos críticos del expected (timestamps/ventana inventados, seguridad afirmada, modificación de inputs): ninguno.

## 4. Redundancia y reservas
- Redundancia moderada: Resumen, "Brecha" y Pregunta 1-3 enumeran lo mismo (ventana, fecha de disponibilidad, código). La última pregunta repite las dos condiciones de Recomendaciones. "Fuente" y "Fuentes leídas" se solapan. Sin secciones duplicadas ni ideas contradictorias. Menos redundante que 0.2.2 (se eliminó el hallazgo del target).
- Reservas de contenido: (a) falta etiqueta/mecanismo explícito por hallazgo, exigido por case.md; (b) "asociación con churn no es mecanismo" solo implícito; (c) redundancia leve Resumen/Brecha/Preguntas; (d) redacción levemente tensa "uso provisional" vs "no usar".
- Alcance: una sola ejecución treatment (modelo haiku-5-5), sin baseline ni generalización. El contrato pasó solo con el límite 650 subido por decisión humana; no lo reinterpreto.

## 5. Veredicto de contenido
**ACEPTABLE CON RESERVAS.** Semánticamente correcto y fiel a las 3 filas y al expediente: sin criterio confirmatorio erróneo, sin falsa invalidez, sin disponibilidad presumida, hashes y ejecución verificados. Las reservas son de completitud formal (mecanismo explícito, asociación/mecanismo) y redundancia leve; ninguna es crítica. No es ACEPTABLE pleno por los dos campos/obligaciones parciales, con criterio coherente con 0.2.2.
