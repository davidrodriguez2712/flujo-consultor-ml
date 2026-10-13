# Revisión de regresiones textuales N01–N03

Fecha: 2026-10-13. Reviewer: agente Codex `/root/native_real02_review`, distinto del autor/runner, conoce las rondas anteriores; no humano ni ciego. Fuentes: cases, inputs, workflow, `.runtime/skill/SKILL.md`, report-context y utility de cada regresión; reportes persistidos y expected privados. No se leen outputs del micro, no se consulta API/red ni se delega. No se editan outputs, criterios o skill.

## Dictamen

**Los tres contenidos conservan el diagnóstico esencial; aprobación con reservas, sin PASS nativo.** N01 y N03 confirman correctamente mecanismos demostrados: la nueva regla de No determinable no los diluye. N02 reconoce válidas identidad y recurrencia en cartera existente, sin falso positivo confirmado; añade una condición documental sobre el año del ajuste que resulta desproporcionada respecto del escenario declarado. N01 contiene un conteo de columnas incorrecto atribuido a la utility, registrado aparte de su diagnóstico correcto.

Son tres ejecuciones textuales distintas, sin control paralelo de versión anterior; no demuestran causalidad, superioridad, generalización ni runtime nativo. No promueven 0.2.1, no alteran la versión canónica ni autorizan gasto/calls posteriores.

## Modo y artefactos observados

El coordinador aclara un override anterior a outputs: guía textual, lecturas autorizadas, única computación con utility fija, hashes reales y persistencia; no plugin Skill nativo. Los tres report-context tienen `mode: textual_guide_not_native`, condición treatment y versión 0.2.1. Los tres reportes declaran explícitamente guía textual y ausencia de invocación/verificación nativa. Cada copia `.runtime/skill/SKILL.md` es byte-idéntica al draft 0.2.1. El modo no figura como clave frontmatter, pero sí en el cuerpo y metadata de contexto: no se disfraza como invocación instalada.

Los case.md originales siguen conservando referencias a whitelist/herramientas/skill instalada y contrato native. El override de ejecución distingue esa instrumentación; no modifica gold. No se afirma ToolPolicy native, aislamiento ni guard verificado. En los archivos inspeccionados no se dispone de stdout/tooltraces o result final que permita comprobar independientemente ejecución exacta de utility, orden de lecturas, ausencia de sobrescritura o límite de 80 palabras del final. Persistencia actual, veracidad semántica y hashes sí son observables; la afirmación de ejecución procede de los reportes y la corroboración del coordinador, no de una traza local examinada.

| Caso | Palabras archivo completo | Filas/columnas reales | SHA-256 reporte |
|---|---:|---:|---|
| N01 | 475 | 3 / 6 | `43f388227b7fbac2d17f7baee7be4f41fa82066c4ea5258e462e6ae84c8c5450` |
| N02 | 551 | 4 / 7 | `6aa190bf0170bf7496bc61f5b07b7747793f35477913e414cb508babe9f64a8e` |
| N03 | 470 | 4 / 5 | `eea959e7ac18ae7e9cc729cff44e5530e367f400e5bfc95d08dbbc9b46c20373` |

Se recomputaron readonly los doce hashes de case/inputs: coinciden con los reportes. Frontmatter físico delimitado, seis claves solicitadas, cinco secciones y límite de 700 palabras cumplidos en artefactos actuales. Fecha 2026-10-13 coincide con el día de evaluación suministrado; no hay started/finished local para atestación temporal adicional. Workflow idéntico en las tres regresiones; prohibición de ampliar autoridad/gates respetada por sus recomendaciones. La utility solo emite hashes/bytes/nombres de columnas/conteos: no mide leakage, performance ni compara tiempos.

## N01: disponibilidad tardía confirmada

Contexto define available_at como primer acceso; A1–A3 tienen hechos terminados el 31 de octubre, scoring el 1 de noviembre a las 08:00 y disponibilidad el 2 de noviembre a las 03:00. Pipeline selecciona payment_sum_previous_day. H1 conecta fuente, uso y demora; no confunde fecha de hechos con acceso. Confianza alta acotada al expediente, severidad alta por impacto temporal y acción de excluir esos valores son fundadas. Propone fuente alternativa solo si realmente accesible y linaje verificable, o cambio de horario autorizado: no backdating ni fuente inventada.

Target futuro retrospectivo se mantiene legítimo. Exportación del 20 de noviembre no se usa como prueba. No certifica split/fit ausentes ni calcula métricas. Todos los slots del único hallazgo material están presentes.

**Reserva media de verificación:** Evidencia afirma que la utility contó «tres filas y siete columnas». El CSV real tiene seis columnas; las tres filas son correctas. El error no invierte el diagnóstico ni demuestra ejecución inventada, pero la afirmación de un check es inexacta y no admite aprobación sin reserva. No se repara el reporte. Tampoco se atribuye a la utility comparación temporal: el reporte la separa correctamente como lectura directa.

## N02: escenario preservado, cautela excesiva

Contexto describe ofertas mensuales para cartera existente, altas posteriores excluidas y client_code conocido antes de septiembre. Pipeline usa identidad y consumo, ajustando encoder/scaler solo con train. CSV muestra dos train y dos evaluation, C1/C2 en ambas, feature previa a scoring y labels train del 9 de octubre anteriores al ajuste declarado del 20. Outcomes evaluation del 9 de noviembre se excluyen de fit y se conservan para backtest.

El informe concluye «No demuestra leakage» y recomienda conservar historia e identidad, delimitar cartera y no extrapolar a altas. No impone GroupKFold ni condena identidad como predictor, y no afirma performance. Los tres hallazgos tienen campos completos y confianza acotada a código/escenario.

**Reserva media de proporcionalidad:** el contexto menciona «20 de octubre» sin año literal, mientras todas las fechas CSV y secuencia operacional son de 2025. Pedir corroborar el año es una cautela documental posible, pero convertirla en condición central de validez y en siguiente paso indispensable exagera una ambigüedad menor. El escenario suministrado sustenta la cronología del expected. No equivale a diagnóstico invertido ni falso positivo confirmado: el propio reporte conserva su validez en lo declarado y no afirma que se usaran labels indisponibles. Debe distinguirse validación externa de producción de respuesta al expediente.

**Reserva baja:** asigna severidad alta a extrapolación/orden real distinto/labels eventualmente indisponibles, hipótesis ajenas al mecanismo observado. Explicita impacto condicional y no probabilidad, pero esa prominencia puede hacer parecer riesgoso un caso válido. La ausencia de código ejecutado permite declarar límites; no exige reinstalar todas las preguntas como condiciones de aprobación del ejemplo.

## N03: contaminación de preprocessing confirmada

Pipeline ajusta scaler sobre todo data antes de máscaras; contexto explica aprendizaje de media/desviación. R3/R4 de noviembre participan en los parámetros que transforman R1/R2 de agosto, pese a entrenamiento declarado el 1 de octubre. El reporte demuestra mecanismo por orden de fit, no por grandes importes, target ni asociación estadística. La disponibilidad de amount al recibir solicitud y madurez de labels train no absuelven el fit global; ambas se preservan como condiciones válidas.

Remedio proporcional: separar primero, fit train-only, parámetros congelados para evaluación y reconstruir backtest. CV/folds se plantea solo si se incorpora después; no exige eliminar outliers ni cambiar scaler. Outcomes evaluation son legítimos retrospectivamente y no se usan en scaler. Confianza alta sobre código declarado, severidad de impacto alta y efecto estadístico desconocido están diferenciados. Todos los campos del único hallazgo aparecen; no se inventa ejecución, estadísticas o nueva fuente. No se encuentra reserva material de contenido.

## Uso de esta evidencia

Conservar resultados originales: N01 correcto en mecanismo con check mal reportado; N02 correcto en escenario con cautela documental excesiva; N03 correcto sin reserva material observada. No existen mecanismos centrales invertidos ni autoridad asumida en el contenido disponible. Los límites de trazas impiden certificar todos los hechos de ejecución. Estos resultados apoyan que el draft puede mantener diagnósticos confirmados y válidos en tres familias, pero no resuelven el gate del micro ni habilitan native. Evaluar después sus diez salidas con la rúbrica fijada, sin rebajar 5/5 treatments ni editar gold.
