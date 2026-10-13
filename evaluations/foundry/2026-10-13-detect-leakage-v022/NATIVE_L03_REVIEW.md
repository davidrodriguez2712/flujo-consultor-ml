# Revisión independiente: detect-leakage 0.2.2, L03 treatment (nativo)

Revisor: agente de IA (no humano) y NO ciego: conozco el propósito de la evaluación, el expected y el fallo previo de 0.2.0. No modifiqué evidencia ni criterios; el contrato sigue FAIL y no lo reinterpreto.

## 0. Verificación de ejecución (stdout.jsonl)
- Cargó la Skill: `tool_use` Skill `acos-eval:detect-leakage` seguido de resultado "Launching skill"; `report-context.json` declara version 0.2.2.
- Ejecutó `check_inputs.py` (Bash real). Su salida devuelve los 4 sha256, bytes, 5 columnas y `rows: 3`, coherente con lo que el reporte declara ("3 filas, 5 columnas"). Leyó workflow.md, case.md, report-context.json y los 3 inputs.
- Sólo herramientas Bash/Read/Skill/Write; no hay red, pipeline ni entrenamiento. No hay ejecuciones inventadas.

## 1. Hashes (recalculados con shasum -a 256)
Los 4 hashes del frontmatter (case.md db7f2572…, context.md ae79d0d6…, dictionary.json 72636cf8…, observations.csv 32ae7c42…) coinciden exactamente con el recálculo sobre `native-package/public/L03`. Fecha 2026-10-13 coherente con timestamps de la ejecución. Sin hashes inventados.

## 2. Cobertura del expected
| Obligación | Estado | Evidencia |
|---|---|---|
| Conclusión No determinable, sin confirmar ni descartar leakage | Presente | Resumen: "No determinable… no puede clasificarse como leakage confirmado ni como temporalmente válida" |
| Export posterior no certifica generación/disponibilidad | Presente | Resumen: "La exportación del 2025-08-01 no demuestra disponibilidad al scoring"; Recomendaciones: "La exportación no la satisface" |
| Pedir ventana, fecha efectiva y código/versión histórica | Presente | Hallazgo 1 acción; Preguntas 1-5 (incl. snapshot al 2025-06-01 y timestamps por reclamo) |
| Condición: reclamos posteriores contaminan / sólo previos y disponibles podría ser válida | Presente | Las dos condiciones en Recomendaciones; Hallazgo 1 las referencia ("ver Recomendaciones") sin repetirlas, como pide la skill |
| No convertir asociación con churn en mecanismo | Parcial | Sólo dice "Con 3 filas no hay inferencia estadística" y "sin evidencia de mecanismo". No nombra explícitamente que la asociación aparente (3→1; pero 2→0) no es mecanismo. Defendible, pero débil |
| Acción proporcional, distinguir reconstrucción de variable intrínsecamente posterior | Presente | "no usar… hasta contar con evidencia"; "snapshot con corte verificable… nunca el valor futuro"; uso bajo autoridad del owner. No rotula "intrínsecamente posterior", pero la distinción reconstrucción/valor futuro está |
| Fundamentación (fuente + mecanismo por conclusión material) | Presente | Cita `context.md` línea 3 (verificado: ahí está "No se conoce si el conteo refleja el estado al scoring o al exportar"), `dictionary.json` (null en feature_available_at/construction_code, verificado) |
| Límites y checks declarados sin sobreafirmar | Presente | "Ejecutado" vs "Leído" vs "No ejecutado"; "datos sintéticos" |
| Campos por hallazgo (componente, mecanismo, fuente, confianza, severidad, acción; exigidos por case.md) | Parcial | H1 completo. H2 sin campo mecanismo explícito. H3 (target) sólo tiene componente, hecho, fuente, acción: faltan mecanismo, confianza y severidad |

## 3. Defectos prohibidos
- Criterio confirmatorio incorrecto: NO. La condición de confirmación exige mecanismo demostrado o disponibilidad efectiva posterior usada como disponible; declara que la exportación no la satisface. Corrige exactamente el fallo de 0.2.0 («un conteo con fecha de exportación confirmaría leakage»).
- Falsa invalidez: NO. No llama inválida a la feature; "no usar… hasta contar con evidencia" es acción provisional condicionada, con "No determinable" preservado en Resumen. Matiz: "Confianza en la brecha alta / en leakage baja" separa correctamente ambas confianzas; "severidad no estimable" es lo que manda la skill.
- Presunción de disponibilidad: NO. Afirma lo contrario (la export no demuestra disponibilidad al 2025-06-01). No usa exported_at como feature_available_at.
- Hashes/ejecuciones inventados: NO (sección 0 y 1).
- Afirmaciones no sustentadas por las 3 filas: NO. Los valores citados (prediction_at idéntico en 3 filas, exported_at 2025-08-01, complaint_count 3/0/2, target 1/0/0) coinciden con el CSV. El mecanismo hipotético de H1 va en condicional ("podría reflejar"), respaldado por context.md.
- Reserva menor: H3 es un "hallazgo" no material (hecho legítimo, no brecha) y aparece comprimido sin campos; es el mismo patrón señalado en 0.2.0 («comprime un hallazgo secundario sin todos sus campos»), aquí atenuado porque H3 no es una brecha.
- "Skill cargada… según report-context.json" es una justificación débil; la prueba real es el tool_use Skill, que sí existe. No es afirmación falsa.

## 4. Contrato: 515 vs 500 palabras (formato puro o contenido)
Es en parte formato y en parte redundancia real, no sólo un desbordamiento aislado de 15 palabras. Conteo por bloque (whitespace): frontmatter 43, Resumen 65, Hallazgos 130, Evidencia 96, Preguntas 67, Recomendaciones 109. Contenido que sobra o se repite (sin reescribir):
- Preguntas 2, 3 y 5 repiten la acción de H1 ("fecha de cada reclamo y snapshot verificable al 2025-06-01") y la acción provisional; Pregunta 4 repite H2 (código/linaje). Hay 4 de 5 preguntas solapadas con Hallazgos/Recomendaciones.
- Resumen repite la ausencia (ventana, fecha de disponibilidad, código) que H1 y H2 vuelven a enumerar, y reitera la acción provisional que Recomendaciones desarrolla.
- H2 re-lista los null de dictionary.json ya contenidos en H1 y en Evidencia.
- H3 (target) es no material y se solapa con Evidencia y el workflow; su eliminación ahorraría ~45 palabras, más que el exceso de 15.
- "Evidencia" repite en "Observado" hechos ya dados en Hallazgos, y la línea "Skill cargada" es redundante con el frontmatter (`skill`/`version`).
Conclusión: el límite no se cumplió porque la receta compacta de la skill (referenciar sin repetir, agrupar) no se aplicó del todo. Es un defecto de contenido leve (redundancia moderada), con un impacto semántico nulo: no hay secciones duplicadas, pero sí ideas repetidas.

## 5. Veredicto
- Contenido: ACEPTABLE CON RESERVAS. Corrige el fallo semántico de 0.2.0 (sin criterio confirmatorio equivocado, sin invalidez, sin disponibilidad presumida, ambas condiciones explícitas, hashes y ejecución verificados). Reservas: (a) H3 sin campos obligatorios de case.md (confianza/severidad/mecanismo) y H2 sin mecanismo explícito; (b) el punto "asociación con churn no es mecanismo" sólo implícito; (c) redundancia entre Resumen/Hallazgos/Preguntas/Recomendaciones.
- Contrato: FAIL (report:word_limit, 515 > 500). No se dispensa ni se reinterpreta el límite. final_words 60/80 cumple; semantic_review REQUIRED queda cubierto por este informe, que no revierte el FAIL.
- Implicación: lo conseguido es una mejora semántica real, pero 0.2.2 no puede declararse pasando L03 mientras el contrato falle; no promover. Este resultado es una sola ejecución treatment (modelo haiku-5-5), sin baseline ni generalización.
