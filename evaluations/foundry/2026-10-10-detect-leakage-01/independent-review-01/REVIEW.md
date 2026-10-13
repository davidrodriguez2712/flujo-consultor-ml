# Revisión independiente — detect-leakage 0.1.0, ronda 05

Fecha: 2026-10-11. Reviewer: agente distinto del autor y del runner. Objeto: evidencia existente; no se ejecutó ninguna nueva evaluación ni se modificaron casos, expected, reportes o Foundry.

## Alcance y método

Leí AGENTS.md de David Skill Foundry, PROTOCOL.md de execution-config-05, los expedientes públicos L01–L03 y sus expected congelados, y metadata.json, stdout.jsonl, audit.md y observed-metrics.json de round-05. No leí author-review.json, otras revisiones ni recomendaciones externas. Los inventarios de nombres de archivos no se usaron como evidencia de contenido. El smoke no se cuenta como caso de eficacia.

Se evaluó significado y evidencia contra obligaciones esenciales, sin exigir frases idénticas o severidades únicas. PASS de contenido requiere mecanismo, cobertura, fundamentación y acción proporcionada; una conclusión material injustificada puede causar FAIL aun si la etiqueta principal es correcta. Los errores de contrato se separan del contenido. «Verificaciones y límites» puede contener evidencia equivalente al encabezado «Evidencia»; su nombre no causa un fallo. No hay umbral congelado de longitud, por lo que brevity es descriptivo, sin PASS/FAIL inventado.

Las referencias siguientes son relativas a evaluations/foundry/2026-10-10-detect-leakage-01. Para abreviar, `R/<rama>` significa `runs/round-05/<rama>/workspace/reports/leakage/audit.md`. Las líneas identifican evidencia; las fuentes públicas y expected citados pertenecen a execution-config-05.

## Resultados por caso y rama

| Caso/rama | Contenido | Formato/trazabilidad del reporte | Runtime | Cumplimiento conjunto |
|---|---|---|---|---|
| L01 baseline | PASS con reservas | PASS | PASS | PASS |
| L01 treatment | PASS con reservas | FAIL | PASS | FAIL |
| L02 baseline | FAIL de fundamentación; conclusión central correcta | FAIL menor de contrato | PASS | FAIL |
| L02 treatment | FAIL de fundamentación/acción; conclusión central correcta | FAIL | PASS | FAIL |
| L03 baseline | PASS con reservas | FAIL menor de contrato | PASS | FAIL |
| L03 treatment | FAIL de fundamentación/acción; incertidumbre central correcta | FAIL | PASS | FAIL |

No detecté ejecución de entrenamiento, pipeline.py, red, edición de inputs, acceso a expected ni aceptación de gates en las llamadas observadas. No clasifico las objeciones de contenido de L02/L03 como falsos positivos **confirmados** de leakage: los reportes evitan afirmar contaminación confirmada. Los FAIL indicados proceden de obligaciones de fundamentación y proporcionalidad, no de inventar un mecanismo confirmado que todos los reportes niegan.

## L01: mecanismo posterior confirmado

**Baseline — PASS de contenido.** H1 cita FEATURE_COLUMNS, generación tras inspección y disponibilidad posterior para S01–S04; reconoce que los ceros tampoco eran conocidos. H3 reconoce historia previa válida. Los límites excluyen split/fit no aportados (R/L01-baseline:64). Se recomienda retirar recovered_kwh y comprobar cortes. La separación feature/outcome se cumple semánticamente con la lista exhaustiva de features, la inspección y el alcance del target, aunque no tiene la explicación tan explícita del treatment. No exijo una frase idéntica a expected.

Reservas: «8 a 11 días» en el resumen es una aproximación; los timestamps reales dan 8,5–11,5 días y la conclusión no cambia. «Solo podría reconsiderarse si se define una versión con corte» (línea 38) no explica que el valor de esa inspección no puede existir antes; debe distinguirse una nueva feature de recuperos históricos, con fuente previa, de filtrar este valor intrínsecamente posterior. La exclusión inmediata es correcta y la alternativa se declara hipotética, por lo que no convierte recovered_kwh en utilizable ni activa una prohibición crítica.

**Treatment — PASS de contenido con reservas.** H1 explica el mismo mecanismo con deltas correctos; excluye la variable intrínsecamente posterior y reconoce historia previa y target fuera de FEATURE_COLUMNS (R/L01-treatment:53). No afirma entrenamiento/performance ejecutados ni concluye sobre split/fit ausentes. Es una resolución esencial correcta.

Reservas: la afirmación «Familias de temporal, de entidad y de join no muestran incidencias» (línea 20) es demasiado amplia e internamente incoherente con el leakage temporal confirmado. La lectura contextual permite entender «temporal» como familia distinta del post-event etiquetado en H1; ese alcance debe aclararse. IDs únicos en cuatro filas tampoco certifican un split de entidades ni ausencia de joins fuera del fragmento. Las preguntas y límites posteriores declaran joins y otras partes no auditables, por lo que trato esta oración como ambigüedad que debe corregirse, no como negación del mecanismo confirmado. Un reviewer más estricto podría marcar FAIL de fundamentación por esa afirmación negativa; esta interpretación no alteraría la recomendación de esta revisión.

**Treatment — FAIL de formato/trazabilidad.** El frontmatter carece de condición. Además «Checks deterministas ejecutados (lectura de CSV y comparación de timestamps)» (línea 48) no distingue inspección manual de ejecución automatizada: metadata/stdout solo muestran una invocación de check_inputs.py, cuya salida informa hashes, tamaños, columnas y filas. No produce comparaciones temporales, cardinalidades ni relaciones feature-target. Esas conclusiones son verificables por lectura, pero no están respaldadas como checks programáticos ejecutados. Baseline sí distingue explícitamente comparación manual. Esta reserva no niega los cálculos correctos; impide aceptar la trazabilidad tal como se redactó.

## L02: historia y entidades conocidas

Los dos reportes cubren features disponibles antes del scoring, etiquetas train anteriores al entrenamiento del 2025-06-01, outcomes de evaluación posteriores usados retrospectivamente, fit sobre train y transform sobre evaluation. No condenan alta señal predictiva ni afirman generalización a producción. Fuentes: public/L02/inputs/context.md, CSV filas de C01–C03 y pipeline.py. La conclusión central «sin leakage confirmado en lo mostrado» es correcta en ambas ramas.

**Baseline — FAIL de fundamentación.** H5 afirma que la ventana target train, hasta 2025-05-08, «no se solapa» con la feature de evaluation cuya ventana termina 2025-06-01 (R/L02-baseline:61). El contexto define esa feature como los 30 días previos al scoring 2025-06-02; esa ventana incluye aproximadamente 2025-05-03–2025-06-01 y sí se superpone al intervalo de outcome de principios de mayo. El endpoint no prueba ausencia de intersección. Esto no implica leakage: al scoring de junio esos consumos son historia disponible y las etiquetas de mayo ya estaban certificadas antes del entrenamiento. La afirmación se ofrece como fundamento material de H5, por lo que incumple el criterio congelado de sustentación, aun cuando entidades conocidas estén correctamente justificadas por operación recurrente.

Reservas: H5 da severidad baja a un riesgo de diseño sin contaminación observada, y H6 identifica falta de aserciones solo como riesgo hipotético del código declarado. Ambas formulaciones delimitadas son aceptables; no las convierto en falso positivo confirmado. Un reviewer que considere la frase de ventanas accesoria podría dar PASS esencial con reserva; explicito el desacuerdo y mantengo FAIL porque el criterio exige soporte de cada conclusión material.

**Treatment — FAIL de fundamentación y proporcionalidad.** H1 dice «Esto no es contaminación si el modelo no usa identidad ni features por cliente» (R/L02-treatment:31); la pregunta 1 dice que su uso «Determina si el solape de entidades es contaminación o dependencia esperada» (línea 67). Esa condición no se desprende del escenario. En scoring recurrente de clientes conocidos, identidad o agregados históricos disponibles no convierten por sí solos el solape en leakage. Haría falta un mecanismo de información no disponible, contaminación del ajuste o un objetivo explícito de generalización a nuevos clientes. La variable de consumo ya es historia por cliente; no puede exigirse excluir genéricamente «features por cliente». Esto debilita una obligación esencial específica de L02, pese a que resumen y recomendación de evaluación separada para clientes nuevos son correctos.

Además `max(prediction_at, train) < min(prediction_at, evaluation)` (línea 57) prueba orden de instantes de scoring de la muestra, no ausencia general de solape de ventanas o contaminación temporal. La validez se sustenta por contexto/disponibilidad de labels y fit train-only, no solo por ese check. No lo trato como leakage confirmado ni exijo GroupKFold.

**Formato.** Baseline posee evidencia real en «Verificaciones y límites» y hashes correctos; no falla por el encabezado. Falla de manera menor porque H2/H3 no explicitan acción recomendada y H4 tampoco la incorpora en el hallazgo, aunque recomendaciones finales permiten inferir mantener el proceso. El contrato pide cada hallazgo con acción, así que separo esa omisión de contenido. Treatment carece de condición en frontmatter y de severidad explícita por algunos hallazgos informativos; la condición ausente basta para FAIL contractual.

## L03: disponibilidad desconocida

**Baseline — PASS de contenido con reservas.** H1 dice «leakage potencial, no demostrado», explica falta de ventana y disponibilidad y pregunta por snapshot, fecha efectiva y código. H2 formula el mecanismo como condicional y recomienda reconstrucción sin usar exportación como prueba de disponibilidad (R/L03-baseline:44). «Qué cambiaría la conclusión» incluye snapshot histórico y verificación real (línea 76). Excluir provisionalmente hasta confirmar es una acción reversible y proporcionada; no es eliminación definitiva prohibida. No exige usar literalmente «No determinable».

Reservas: confianza «media en que haya leakage real» (línea 34) no puede deducirse de esos datos; lo sustentado es alta confianza en la **insuficiencia** de evidencia. El resumen «no puede considerarse disponible ... con la evidencia» se interpreta como imposibilidad de acreditar disponibilidad, no como prueba de inexistencia de la feature. Un reviewer puede leerlo como sobreafirmación y marcar FAIL; H1, condicionales y límites favorecen la interpretación de incertidumbre. No registra una fecha inventada ni confirma leakage por exported_at. Falta acción para H4 metadata, por lo que formato recibe FAIL menor aun con estructura, condición y hashes correctos.

**Treatment — FAIL de fundamentación/acción, aunque acierta la clase central.** Estado y confianza son «No determinable», y las preguntas sobre disponibilidad, ventana e histórico son útiles. No usa exported_at como timestamp real de disponibilidad. Sin embargo:

- «Si se construyó hasta 2025-06-01, no hay leakage temporal» (R/L03-treatment:28) omite la disponibilidad efectiva al scoring. Un conteo de eventos anteriores puede calcularse o ingresar después. Las preguntas sobre disponibilidad mitigan el error, pero no justifican esa conclusión condicional suficiente.
- «No hay igualdad ni mapeo 1:1: no se detecta target leakage directo» (línea 51) no demuestra ausencia de un mecanismo. Una feature derivada del outcome puede ser transformada o ruidosa; tres pares de valores solo sustentan observaciones descriptivas. No hay prueba de linaje o construcción. Incluso «mapeo 1:1» es ambiguo: los valores únicos permiten mapearlos al target en esta muestra, aunque la relación no sea biyectiva. La incertidumbre general no autoriza exonerar una familia específica por ese test.
- «Verificar split temporal y ausencia de solape de clientes» (línea 71) prescribe un requisito sin esquema ni población operativa aportados. Puede requerirse para clientes nuevos; puede ser improcedente para clientes conocidos. Lo proporcionado sería solicitar escenario y justificación del split. Este caso pide auditar complaint_count, no imponer una validación por entidad no sustentada.

No marco fallo crítico por confirmar leakage o afirmar seguridad completa: el reporte no hace ninguna de esas dos cosas globalmente. Marco FAIL ordinario por conclusiones materiales y una acción injustificadas. Si otro reviewer entiende esas frases como observaciones limitadas y recomendaciones opcionales, puede dar PASS esencial con reservas; aun así formato seguiría FAIL y no habría señal favorable bajo la regla congelada.

Formato treatment: condición ausente; versión expresada como «0.1.0 (según plantilla ... no verificada en runtime)», no como identificador inequívoco verificado. La invocación nativa sí se observa en stdout/metadata. No infiero hash exacto de la skill desde el reporte ni certifico snapshot/instalación sin leer material fuera del alcance.

## Persistencia, trazabilidad y runtime

Recalculé con stdlib los SHA-256 de expedientes públicos y de los seis audit.md: coinciden con hashes de reportes/inputs en metadata, observaciones métricas y los reportes. Las fechas 2026-10-11 coinciden con started_at/finished_at. La evidencia permitida demuestra archivos persistidos y una única llamada Write por rama. No contiene una comprobación independiente del estado inicial del filesystem; por ello no certifico ausencia previa absoluta ni aislamiento efectivo completo. No se observan sobrescrituras repetidas en la traza.

En stdout, system/init declara claude-haiku-5-5, herramientas Bash/Read/Skill/Write y permiso dontAsk. Treatment incluye acos-eval:detect-leakage en skills y registra Skill más «Launching skill»; baseline no incluye esa skill ni la invoca. Las ramas comparten modelo, esfuerzo low, herramientas y prompt visible en argv, con plugin-dir y permisos de lectura del plugin como diferencia treatment. También aparecen doctor y plugin-authoring en ambos entornos: no afirmo que no existiera ninguna otra skill. No hay llamadas observadas a esas skills auxiliares.

Seis metadata registran runtime_success true, returncode 0, report_persisted true, cuatro requests por ejecución. stdout/result es success sin error. El número num_turns de stdout (9 baseline, 10 treatment) no se debe confundir con request_count 4 ni atribuir un fallo por exceder max-turns 8 sin conocer la semántica del runtime. Runtime PASS describe éxito técnico y persistencia, no calidad ni aislamiento demostrado.

## Brevity y coste, separados del contenido

Datos de observed-metrics.json; costes estimados, no nueva facturación. Output incluye tokens de generación del runtime, no equivale a palabras del reporte ni debe sumarse de nuevo thinking_subset.

| Caso | Palabras baseline → treatment | Segundos baseline → treatment | Output tokens baseline → treatment | USD estimados baseline → treatment |
|---|---:|---:|---:|---:|
| L01 | 683 → 839 | 23,05 → 29,94 | 4853 → 6036 | 0,003999 → 0,006160 |
| L02 | 763 → 917 | 30,19 → 31,12 | 6351 → 6218 | 0,004959 → 0,006298 |
| L03 | 705 → 792 | 23,68 → 23,54 | 4903 → 4709 | 0,003978 → 0,005281 |

Treatment es más largo en los tres reportes, incorpora familias no aportadas y preguntas sobre métricas fuera de la auditoría. Los resúmenes finales son breves y dan ruta. No existe umbral de palabras congelado: no asigno un FAIL de brevity. Treatment cuesta más en todos los casos; la latencia aumenta en L01/L02 y es prácticamente igual en L03. Una sola ejecución por rama no acredita diferencias estables.

## Recomendación y límites de independencia

No se observa la señal favorable definida en PROTOCOL.md: treatment no mejora cumplimiento conjunto en al menos dos casos y no conserva el cumplimiento contractual de baseline. Baseline ya resuelve las clases centrales de los tres casos, aunque tiene errores de detalle; hay efecto techo en detección/clasificación esencial, no cumplimiento perfecto del baseline. El treatment formula más explícitamente la incertidumbre de L03 y la imposibilidad de recuperar el valor post-inspección en L01, pero añade condiciones sobre entidades, inferencias negativas y omisiones de trazabilidad. Esa mejora de redacción no satisface la regla de eficacia.

Recomiendo mantener detect-leakage 0.1.0 como experimental y supervisada, corregir las afirmaciones de temporalidad/entidades y el contrato de trazabilidad en una versión futura, y evaluar esa versión con criterios predefinidos y casos adicionales. Conservar esta evidencia y expected sin alterarlos. Antes de una decisión de madurez, un humano debería adjudicar los desacuerdos de interpretación señalados. Esta revisión no promueve ninguna capacidad ni declara estabilidad o generalización.

La independencia es limitada: soy un agente distinto del autor/runner, no un reviewer humano. Conozco los nombres baseline/treatment, por lo que la revisión no es ciega a la condición. Es una revisión LLM de tres casos sintéticos con una ejecución por rama; no elimina sesgos comunes de agentes ni prueba causalmente una ventaja general de la skill. No leí la revisión del autor para formar el juicio; las recomendaciones anteriores son propias. El alcance de archivos permitido limita la verificación del aislamiento, del snapshot exacto de skill y del estado inicial de escritura. La autoridad final permanece en el usuario.
