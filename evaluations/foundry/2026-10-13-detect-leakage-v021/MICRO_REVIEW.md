# Revisión independiente del micro textual 0.2.0/0.2.1

Fecha: 2026-10-13. Reviewer: agente Codex `/root/native_real02_review`, distinto del autor/runner. Conoce el propósito del parche, casos y cohortes anteriores; no es humano ni ciego. Se revisaron las diez salidas originales, sus response.sse, micro-package02/task/guías/runner/manifest, approval, ledger/summary y rúbrica/expected privados fijados. No API/red, entrenamiento, delegación, reparaciones ni cambio de gold/canonical/estado.

## Dictamen y gate

**Gate NO satisfecho; no justifica pasar a native L03 bajo el protocolo predeclarado.** La condición exige 5/5 treatments sin criterio de confirmación incorrecto, invalidez falsa o disponibilidad presumida, además de contrato completo. Solo **1/5 treatments** cumple el contrato de 250 palabras. Cuatro exceden el límite y no se descuentan palabras de metadata ni se recorta texto. Existen asimismo reservas de cobertura/semántica. Una valoración favorable de parte del contenido no dispensa el gate.

Los controles reciben idénticos criterios: 2/5 cumplen el contrato. Son controles con guía textual 0.2.0, no baseline sin skill. El micro muestra respuestas más explícitas sobre incertidumbre en varias salidas 0.2.1; no establece corrección consistente completa, superioridad causal de la skill ni generalización. Una única situación repetida y diez respuestas no acreditan runtime native o validez estable.

## Identidad, protocolo y transporte

Las guías del micro-package02 coinciden byte por byte con snapshot 0.2.0 y draft 0.2.1. Comparado con el task de preparación inicial, el único cambio es la aclaración mecánica del inicio físico `---`, cierre de metadata, siguiente sección y ausencia de fences/texto externo. El expediente y la pregunta semántica permanecen iguales; package01 no se contabiliza como ejecución. Las entradas del manifest recomputadas coinciden y su hash coincide con micro-approval.

El runner construye una request fresca por muestra, sin historial de outputs, tools o expected; usa mismo task/modelo/cap 3072 y alterna orden de brazos entre repeticiones. Incorpora guía seleccionada, versión y fecha UTC real al system. Esa fecha es 2026-10-13 en todas las salidas. Se observa `modo: guia_textual`, versiones correspondientes, skill detect-leakage y los tres nombres de inputs correctos. No se exige hash ni se interpreta guía textual como instalación/invocación nativa.

Las diez output.md son idénticas al concatenado de text_delta de response.sse, sin reparaciones observadas. Todas terminan end_turn, sin bloques tool_use. Ledger tiene diez entradas HTTP 200/end_turn, ningún tool_guard_error y cero rechazos. Summary acredita transporte completo pendiente de contenido; no PASS semántico. No hubo truncación declarada por stop_reason. La extensión excesiva no se excusa por cap ni por transporte exitoso.

## Matriz de revisión

Semántica **S**: obligaciones esenciales cubiertas, con reservas menores; **P**: parcial por brecha de cobertura o acción ambigua; **F**: defecto material en criterio/conclusión/acción. No son score compuesto ni reemplazan hallazgos. Todos tienen un único documento, delimitadores físicos, seis campos frontmatter, nombres/version/fecha/modo adecuados y cinco secciones. El contrato mostrado falla únicamente por longitud cuando se indica FAIL.

| Repetición | Guía | Palabras wholefile | Contrato ≤250 | Semántica | Fundamento principal |
|---|---|---:|---|---|---|
| 01 | 0.2.0 | 262 | FAIL | F | Condena como no válido si solo existe conteo de exportación; fuente tardía no demuestra invalidez. |
| 01 | 0.2.1 | 313 | FAIL | S | No determinable; export no fecha feature; confirmación por eventos posteriores, posible validez con ventana y disponibilidad. |
| 02 | 0.2.0 | 250 | PASS | P | Buena brecha/posible validez; riesgo alto sin separar impacto y condición explícita de confirmación ausente. |
| 02 | 0.2.1 | 292 | FAIL | P | No determinable sustentado y posible validez conjunta; condición de confirmación no se desarrolla explícitamente. |
| 03 | 0.2.0 | 260 | FAIL | F | «Snapshot posterior (Probable)» atribuye probabilidad de contaminación sin mecanismo/evidencia de construcción. |
| 03 | 0.2.1 | 293 | FAIL | P | Distinción export/feature y posible validez claras; falta condición explícita de confirmación y versión histórica en preguntas. |
| 04 | 0.2.0 | 239 | PASS | F | «Evaluar sin outcomes posteriores» contradice el backtest legítimo; blocking de uso sin autoridad explícita. |
| 04 | 0.2.1 | 204 | PASS | P | Incertidumbre/validez conjunta; severidad alta justificada por exportación tardía y distinción export/disponibilidad incompleta. |
| 05 | 0.2.0 | 296 | FAIL | P | Brechas y validez condicional correctas; ventana previa debe explicitarse y falta condición de confirmación. |
| 05 | 0.2.1 | 285 | FAIL | P | Ventana/disponibilidad y confirmación correctas; reservar predictor «solo para evaluación retrospectiva» deja uso ilegítimo ambiguo. |

## Hallazgos de contenido por brazo

**0.2.1, repetición 01:** cubre mejor la cadena de decisión. No afirma invalidez ni seguridad; pide ventana, disponibilidad, código y versión histórica, limita severidad a impacto posible y reserva uso bajo owner. No fecha el valor por exported_at. Confirmar uso de reclamos posteriores es correcto; validez provisional necesita ventana/fechas previas y disponibilidad al scoring. «Lectura ... no ejecutada» se interpreta como ausencia de ejecución de tools, no como verificación automatizada. Las fechas resumidas no inventan timestamps. El uso de ≤ en reclamos debe entenderse contra el cutoff completo suministrado; no acredita ventana por día calendario solo. Reserva menor: no explicita legitimidad de target retrospectivo, aunque tampoco lo condena ni lo convierte en predictor. Contrato incumplido por 63 palabras.

**0.2.1, repeticiones 02/03:** preservan incertidumbre y no presumen disponibilidad. 02 dice explícitamente que export solo fecha archivo; 03 dice que export no fecha feature. Ambas exigen ventana previa y disponibilidad, y preguntas de linaje. No presentan una condición de confirmación incorrecta, pero omiten explicar qué evidencia confirmaría contaminación, mientras sí explican posible validez. Es cobertura parcial del expected, no falso positivo confirmado. Pedir split/preprocessing en 02 es ajeno al expediente acotado; 03 llama «correlación» a un ejemplo U01 sin cálculo, aunque lo limita a no probar leakage/generalización. Reservas de precisión, no performance inventada. Los excesos son 42/43 palabras.

**0.2.1, repetición 04:** único contrato conforme. H1 sostiene severidad potencial alta «porque la exportación es posterior al scoring». Fecha de exportación no demuestra información futura ni disponibilidad posterior; severidad puede justificarse por impacto potencial de reclamos posteriores si se explicita esa condición. Aquí falta la distinción decisoria export/disponibilidad y condición de confirmación, aunque la conclusión no confirma leakage actual y pide ambas fechas. La igualdad no universal feature-target se observa correctamente en tres filas y no se usa para descartar leakage. Fuente de brecha/confianza se comunica por secciones; no se exige reiterar la misma cita en cada línea. Defecto de fundamento/cobertura, sin convertirlo en falsa confirmación actual.

**0.2.1, repetición 05:** declara que no puede concluir validez ni invalidez, impacto potencial condicionado y dos direcciones de decisión correctas: reclamos posteriores invalidan como predictor; solo previos y disponibles permitirían uso. «Reservarlo solo para evaluación retrospectiva» es ambiguo y reproduce una reserva conocida: complaint_count es predictor propuesto, no outcome. Puede conservarse para descripción retrospectiva; no se debe implicar que una feature indisponible sea legítima como predictor de backtest por hacerlo retrospectivo. Target posterior sí es outcome legítimo. No se cuenta esa frase como instrucción explícita de entrenar con futuro, pero impide aceptación sin reserva de accionabilidad. Exceso de 35 palabras.

**0.2.0, repetición 01:** además del exceso de 12 palabras, «Si solo existe el conteo de exportación, tratarlo como no válido» cambia falta de evidencia por invalidez. No se demuestra generación/uso tardío solo por existir export. Su condición de posible validez sí pide disponibilidad y ventana previas; no salva la condición incorrecta. Las severidades altas deben distinguir impacto de sospecha/probabilidad.

**0.2.0, repetición 02:** contrato exactamente 250, sin margen ni descuento. Mantiene riesgo no confirmado y pide ventana, disponibilidad y fuente histórica. «Riesgo alto» no distingue impacto/probabilidad, y omite condición confirmatoria; no atribuye fecha export a disponibilidad. La reconstrucción con snapshot se propone como acción, pero debería condicionarse a fuente histórica real. No declara seguro ni inválido el predictor actual.

**0.2.0, repetición 03:** exceso de 10 palabras. Clasifica snapshot posterior como «Probable» y sospecha material por estado al exportar, aunque esa posibilidad no demuestra probabilidad ni contaminación. Debe quedar como brecha No determinable. La condición de validez exige ventana/disponibilidad/código; no confirma explícitamente leakage actual.

**0.2.0, repetición 04:** no excede extensión. Reconstrucción histórica y validez conjunta son coherentes, pero «evaluar sin outcomes posteriores» elimina los resultados futuros legítimos necesarios para backtest. Distinguir outcomes de features es esencial para acción proporcional. «Bloquear» su uso también asume más decisión que proponer reserva provisional al owner. No se observa acción externa ejecutada; se evalúa el consejo incorrecto, no una violación de producción materializada.

**0.2.0, repetición 05:** exceso de 46 palabras. Explicita que export no prueba disponibilidad, pide tres brechas y no usa ausencia de igualdad para certificar seguridad. «Ventana con cutoff verificable» debería exigir explícitamente hechos previos, no solo corte verificable de cualquier fecha. Falta condición de confirmación. La frase no ejecutado conteos se interpreta como no herramientas; tres filas leídas no requieren tools ni forman claim de entrenamiento.

## Decisión y saldo

Coste observado micro 0.0082625 USD, dentro de subpresupuesto 0.0165. Approval indica prior 0.115103045 y techo acumulado 0.15; suma observada tras micro 0.123365545, saldo aritmético 0.026634455. Son datos de approval/ledger y cálculo, no tracker global ni renovación de autorización. No se leyó clave ni env.

**No procede native L03 bajo este gate**, aun con saldo positivo: no hay 5/5 contratos y no hay cobertura semántica integral repetida. Conservar el micro mixto y todos sus originales; no reparar, recortar, cambiar etiquetas o ampliar el límite para aprobarlo. Una corrección o nueva ronda exigiría protocolo nuevo identificable y autorización aplicable; esta revisión no la concede. Mantener canonical 0.2.0 y draft 0.2.1 experimental, sin promoción.
