# Revisión de preparación — detect-leakage 0.2.0

Fecha: 2026-10-11. Reviewer: agente distinto del autor. Alcance: draft/skills/detect-leakage/SKILL.md, cases/N01–N03 con sus inputs, reviewer/N01–N03/expected.md y templates/SKILL.md, case.md y expected.md del Foundry. También se aplica AGENTS.md del Foundry ya leído. No se generaron outputs evaluados, no hubo llamadas API/red, ni cambios a skill/cases/expected. Este archivo es el único artefacto nuevo de esta revisión.

## Dictamen de preparación

**El contenido del borrador es apto como hipótesis experimental; la ejecución debe esperar a cerrar los bloqueos de contrato e interpretación señalados.** No hay un error central demostrado en los mecanismos de los tres fixtures. No se afirma eficacia, calidad de outputs, estabilidad ni generalización de 0.2.0: todavía no se observaron ejecuciones de esta versión.

| Artefacto | Juicio de preparación | Evidencia principal |
|---|---|---|
| Skill 0.2.0 | Coherente y generalizable; pendiente operacional del caller | Workflow, Checks, Output, Verificación final |
| N01 | Mecanismo verificable; contrato runtime pendiente | Ventana pasada y available_at posterior en 3/3 filas |
| N02 | Diagnóstico esperado sustentado, limitado al escenario declarado | Cartera existente, ID previo y fit train-only |
| N03 | Fit global verificable; aclarar obligación de CV ausente | fit_transform(data) antes de separar particiones |
| Expected | Evaluación semántica prevista; ambigüedades por resolver antes de freeze final | Obligaciones amplias y caso N03 CV |

Las rutas de evidencia siguientes se refieren a evaluations/foundry/2026-10-11-detect-leakage-v02, salvo templates del Foundry.

## Correcciones reutilizables y ausencia de respuestas particulares

El borrador separa hechos pasados, cálculo y disponibilidad efectiva; no infiere disponibilidad desde exportación. Trata recurrencia según población operacional; no condiciona automáticamente la validez a excluir identidad o features por cliente. Explica que ventanas solapadas no prueban leakage. Exige linaje/mecanismo para interpretar señal perfecta o ausencia de igualdad. También separa checks ejecutados de inspección y reconoce que más filas no resuelven desconocimiento de proceso. Estas reglas corrigen familias de errores observadas, no solo una respuesta puntual.

No encontré nombres N01/N02/N03, fechas o valores de fixtures, payment_sum_previous_day, client_code, usage_previous_30d ni amount en la skill. No contiene la secuencia de clases esperadas de los casos ni rutas de expected. «Un dato pasado puede llegar tarde» y «un cliente recurrente puede ser parte válida» son principios generales del problema, no una enseñanza de resultados particulares. Que los casos estén construidos para ejercitar esas reglas limita su fuerza como evidencia de generalización; no invalida el diseño como regresiones iniciales.

Output da prioridad al contrato del caller, incluye condición cuando se pide, exige listar campos/ruta/extensión y evita duplicar reporte en respuesta final. No afirma verificación del runtime sin evidencia. Preconditions distingue permiso de capacidad y permite completar partes independientes. Son correcciones aplicables a otras auditorías.

Reserva: «Una feature previa es válida solo si también estaba disponible» expresa una condición necesaria, no certificación suficiente. Debe interpretarse junto con rastreo de construcción y fit; no como una regla que descarte otras familias de leakage. Asimismo los estados Confirmado/Probable/Riesgo/No determinable están enumerados pero no definidos operacionalmente. Conviene precisar que Confirmado califica un mecanismo observado, Riesgo una posibilidad condicionada y No determinable una brecha; no es bloqueo del mecanismo de estos fixtures, pero reduce consistencia entre reviewers.

## Requisitos del template Foundry

La skill declara name, description, status experimental, version 0.2.0 y domain; contiene propósito, uso/no uso, inputs, preconditions, workflow, checks, reglas, output, verificación, modos de fallo, límites y referencias. Cumple los componentes sustantivos del template. Inputs distingue obligatorios de deseables en prosa; workflow usa una lista numerada en vez de subsecciones; modos de fallo utiliza causa/mitigación compactas. No considero estas diferencias de formato incumplimiento: AGENTS.md exige definir esos elementos, no copiar encabezados internos o texto placeholder literalmente.

Cases tienen metadata y Contexto, Objetivo, Tarea, Inputs, Restricciones y Criterio de finalización. Expected tienen metadata, comportamiento, hallazgos críticos/importantes/opcionales, evidencia, comportamientos incorrectos, fallos críticos, cuatro dimensiones de calidad y notas. La estructura está alineada al template, con expected separado de material público. Las notas prohíben buscar frases y cambiar criterios para favorecer outputs. Esa declaración no demuestra aún aislamiento ni congelamiento efectivo del runtime.

## Evidencia y ambigüedades por fixture

### N01 — historia que llega tarde

cases/N01/inputs/context.md define period_end como fin de hechos y available_at como primer acceso del motor. CSV: scoring 2025-11-01T08:00:00Z; period_end 2025-10-31T23:59:00Z; available_at 2025-11-02T03:00:00Z en A1–A3. El atraso es 19 horas en las tres filas, aunque los hechos son pasados. pipeline.py incluye payment_sum_previous_day. Expected pide ese mecanismo, evita inferencia desde outcome, requiere fuente/snapshot disponible o cambio de horario bajo autoridad y no certifica split/fit ausentes. Está sustentado.

No es necesario usar el nombre «post-event» ni condenar la historia por su asociación con target. Filtrar period_end no arregla llegada tardía; una fuente alternativa o mover decisión son hipótesis, no hechos. El contexto menciona exportación el 20 de noviembre sin año explícito, pero la disponibilidad está fechada completamente en CSV: no hace falta inferir año para resolver. No convertirlo en requisito de timestamps adicionales.

### N02 — identidad legítima en cartera existente

Contexto define ofertas sobre cartera existente, altas nuevas fuera de evaluación y client_code existente antes de septiembre. En CSV hay dos IDs en ambas particiones; usage disponible antes de scoring; labels train 2025-10-09 antes del entrenamiento del 20 de octubre; evaluación de noviembre posterior. pipeline.py separa particiones antes de ajustar encoder y scaler, y solo transforma evaluación. Expected permite límites de código real sin condenar automáticamente ID/feature/split. Está sustentado.

Ambigüedad no bloqueante: no se especifica clase de encoder/scaler. La firma visible no recibe target y el expediente presenta un orden declarado; permite juzgar fit train-only de lo mostrado, no certificar implementaciones internas, estado previo, generalización o métricas. No exigir pruebas de una contaminación oculta no aportada. El 20 de octubre no tiene hora/zona explícita; las etiquetas son del día 9, así que el orden necesario es inequívoco sin inventar una hora de entrenamiento.

### N03 — ajuste global antes de particionar

pipeline.py aplica scaler.fit_transform a data[["amount"]] antes de separar train y evaluation; por tanto el ajuste recibe ambas particiones, incluyendo solicitudes futuras de noviembre respecto del entrenamiento del 1 de octubre. Contexto declara amount disponible al recibir solicitud y labels train ya maduros. CSV diferencia importes train 100/200 de evaluation 9000/12000. Expected acierta al localizar contaminación en parámetros aprendidos, no en que amount fuera intrínsecamente futuro para su propio scoring. El remedio es fit train-only y transform evaluation; no eliminar outliers o cambiar de scaler.

La clase concreta del scaler no permite calcular parámetros ni magnitud del efecto; no debe exigirse demostrar un aumento de performance. «Confirmado por código» se entiende como inclusión de evaluación en el ajuste de una transformación aprendida declarada, no como entrenamiento real ejecutado. Tampoco se aporta una fecha exacta de disponibilidad por fila: contexto basta para la afirmación acotada, no autoriza crear timestamps.

## Bloqueos concretos antes de ejecución

1. **Completar y congelar contexto/utility del runtime.** Los tres case.md requieren leer `.runtime/report-context.json` «suministrado» y ejecutar una utility fija. Esos artefactos y su schema/comando no están en los fixtures revisados. Antes de invocar se debe crear/verificar el contexto por rama, sin respuestas particulares, y definir la utility readonly, comando, outputs genéricos, permisos y hashing. La autorización de lectura pública enumera inputs/case/report-context; si el runner necesita que el agente lea workflow.md o el código de utility, esas lecturas deben estar cubiertas expresamente por el contrato común. No declaro que el futuro runner carezca de ello: el paquete leído no lo demuestra.
2. **Fijar skill/version de baseline.** El contrato pide skill y version para todas las ramas, pero no especifica none/null para baseline ni qué valores de condición admite report-context. La skill treatment ofrece su versión; baseline no puede atribuírsela. Debe suministrarse esa regla en contexto común visible para ambas ramas y congelar el schema antes de ejecutar. No se debe adjudicar un formato nuevo después de ver outputs. También resolver cómo identificar fecha real en runtime y qué archivos de inputs se incluyen en hashes (case y report-context, además de inputs, si se requieren).
3. **Congelar conteo y alcance de límites.** «máximo700palabras total; resumen≤80palabras y ruta» no especifica si total incluye frontmatter/response final, ni si resumen es sección del reporte, respuesta final o ambos. Definir antes de outputs un conteo reproducible, por ejemplo tokens separados por whitespace en todo audit.md incluido frontmatter, y un límite independiente de 80 en la respuesta final excluida la ruta. Es un ejemplo de regla posible, no una imposición ni criterio retroactivo. Si se pretende otra interpretación debe quedar explícita. La longitud debe juzgarse aparte de contenido.
4. **Desambiguar CV en expected N03.** Comportamiento esperado incluye «en CV dentrofold» y Correctitud exige todos sus elementos, aunque no hay CV en el fixture y Cobertura prohíbe exigir familias ausentes. Antes de freeze final, declarar ese remedio condicional/opcional («si se implementa CV») o quitarlo del conjunto esencial. No penalizar un reporte que arregle fit global con train/transform y omita CV ausente. Esta revisión no modifica expected.

Los puntos 1–3 son bloqueos de reproducibilidad/contrato, no evidencia de que la skill falle. El punto 4 bloquea una adjudicación inequívoca del caso N03 si se mantiene como obligación literal. Se pueden cerrar con preparación local autorizada antes de cualquier llamada; no requieren producir outputs evaluados.

## Aclaraciones recomendadas, sin cambiar diagnósticos

Expected repite «Cubrir mecanismo esencial sin ... confirmar riesgo inexistente»: riesgos plausibles pero no confirmados deben distinguirse de hallazgos confirmados; no convertir una pregunta delimitada en falso positivo crítico. En N02 especialmente, admitir una preocupación explícita sobre otro escenario sin condicionar la validez actual. «Citas exactas» debería significar referencias precisas que soportan el mecanismo, no citas textuales obligatorias, pues las notas exigen juicio semántico.

«Fecha o check inventado» es criterio crítico amplio: distinguir timestamp fabricado de un error tipográfico no material, y ejecución atribuida sin traza de una comparación manual declarada. No se exige que el agente automatice tiempos o relaciones si solo está permitido ejecutar una utility de hashes/conteos. Ninguna frase del reporte debe decir que esa utility determinó leakage.

Antes de ejecutar también deben demostrarse configuración idéntica salvo skill, modelo/versión, orden de ramas, aislamiento de expected, ausencia inicial del reporte, instalación/invocación real y presupuesto/autorización. No revisé configuración de runner en este encargo; son pendientes de evidencia técnica, no fallos demostrados del paquete ni autorización para llamadas pagadas. Conservar snapshots/hashes y expected final antes de outputs.

## Recomendación y límites de independencia

Cerrar los cuatro bloqueos anteriores y congelar sus soluciones antes de ejecutar. Mantener N01–N03 como casos iniciales/regresiones: tienen evidencia suficiente para sus clases centrales y no requieren performance. Ejecutar después con baseline/treatment comparables, reportando contenido, contrato, brevity y runtime por separado. No inferir calidad ni estabilidad del borrador por esta revisión; una evaluación posterior debe reconocer que los casos fueron diseñados para ejercitar correcciones conocidas.

Revisión realizada por un agente distinto del autor/runner, no por un humano. No es ciega al propósito de 0.2.0 ni a la relación con fallos previos: participé en la revisión de ronda 05 y conozco esas familias de errores. No he observado outputs nuevos ni afirmo independencia de diseño de los fixtures, congelamiento efectivo o ausencia de contaminación del runner. No modifiqué artefactos evaluables, no ejecuté pipelines, no autoricé una llamada API ni promoví una capacidad. La decisión final permanece en el usuario.
