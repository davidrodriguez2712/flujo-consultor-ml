# Registro de hipótesis de capacidades para ACOS

**Estado:** registro exploratorio; 24 fichas canónicas con 18 decisiones de mantener como conocimiento y seis diferidas (revisión del 6 de octubre de 2026)  
**Fecha:** 4 de octubre de 2026  
**Fuente actual:** [veinticuatro escenarios hipotéticos E2E](2026-10-04-acos-business-simulations.md)

## Cómo leer el registro

H01–H24 son identificadores de hipótesis, no estados ni IDs canónicos del Foundry. Los nombres son provisionales. Estas entradas son descripciones de hipótesis, no instrucciones operativas ni decisiones de promoción. Los experimentos posteriores asociados se consultan en el Foundry y en la revisión actual enlazada. Cada entrada conserva lo que podría ser reusable y qué habría que verificar para elegir entre skill, extensión de una skill, playbook, template o gate.

Las 24 entradas tienen fichas canónicas con metadata `status: candidate` en el Foundry. Su decisión actual es mantener como conocimiento (18) o pendiente/diferido (6); la metadata por sí sola no implica elegibilidad operativa. Véase la [revisión actual de integración](2026-10-06-acos-foundry-integration.md). El [mapa de candidates](2026-10-04-acos-foundry-candidate-map.md) enlaza cada ficha y registra el tratamiento propuesto tras revisar solapamientos. H01–H24 se mantienen como IDs de procedencia, no sustituyen los IDs del Foundry.

La base inicial fue el análisis de escenarios y su contraste con el inventario y los playbooks. Después se registraron decisiones y experimentos en el Foundry; la revisión actual enlazada distingue lo evaluado de las hipótesis diferidas. Los bullets siguientes preservan el diseño inicial, no reemplazan esas decisiones ni declaran nuevas evaluaciones pendientes por defecto. Un caso sintético puede ayudar a probar una hipótesis; no representa un proyecto real ni demuestra frecuencia de uso.

## H01 — `frame-business-decision`

- **Trigger/problema:** brief ambiguo que lleva a elegir tecnología antes de precisar la decisión.
- **Inputs → output:** contexto, stakeholders, acciones y restricciones → decisión, owner, unidad, horizonte, métricas, scope y preguntas abiertas.
- **Check propuesto:** identifica información faltante sin inventar KPI/owner; explica cómo el resultado cambia una acción.
- **Escenarios:** C1–C24; comparar especialmente C1, C8, C14, C17 y C7.
- **Artefacto/límite:** posible skill frente al brief/gate existente; no sustituye la aprobación del stakeholder ni todo el lifecycle del OS.

## H02 — `quantify-decision-impact`

- **Trigger/problema:** una recomendación técnica no tiene comparación explícita de valor, coste y supuestos.
- **Inputs → output:** política actual/propuesta, costes, outcomes, capacidad y evidencia disponible → escenarios de impacto, baseline, sensibilidad e incertidumbre.
- **Check propuesto:** distingue resultados observados, simulados y esperados; no inventa costes ni afirma causalidad sin diseño pertinente.
- **Escenarios:** C1–C7, C10–C13, C15/C16 y C19–C21; C17/C18 si se comparan escenarios de valor/riesgo con inputs suficientes. C22/C23 cuando se comparan valor, costes y políticas; C24 solo con inputs de valor operacional suficientes.
- **Artefacto/límite:** posible skill de análisis condicionado frente al playbook de impacto; no obliga a calcular ROI en todos los engagements.

## H03 — `formulate-constrained-decision`

- **Trigger/problema:** se propone optimizar sin precisar qué decisiones, objetivos o restricciones son válidos.
- **Inputs → output:** acciones, recursos, datos y restricciones provistas → variables de decisión, objetivo, restricciones, factibilidad, escenarios y vacíos.
- **Check propuesto:** separa restricciones duras/blandas y decisiones/supuestos; detecta incompatibilidad o información insuficiente.
- **Escenarios:** C2–C5, C12, C15 y C19. C22–C24 cuando existe asignación de presupuesto o capacidad.
- **Artefacto/límite:** posible skill de formulación; no selecciona un solver ni ejecuta asignaciones externas por defecto.

## H04 — `design-intervention-evaluation`

- **Trigger/problema:** se interpreta una predicción o comparación histórica como efecto de una intervención.
- **Inputs → output:** intervención, población, asignación viable, outcomes y restricciones → estimand, unidades, diseño, supuestos, guardrails y plan de análisis.
- **Check propuesto:** aborda selección, interferencia y cumplimiento; indica requisitos de precisión/potencia y no inventa inputs para calcularlos.
- **Escenarios:** C1, C3, C11, C13 y C19; C20/C21 cuando se evalúa efecto de una intervención. Variar asignación individual versus tiendas/grupos. C23; C22 si se evalúa efecto de invertir en retención o adquisición.
- **Artefacto/límite:** posible skill frente al playbook de experimentación; `design-validation` no cubre esta responsabilidad.

## H05 — `evaluate-operational-selection`

- **Trigger/problema:** un score se evalúa sin representar la política de intervención y su capacidad.
- **Inputs → output:** scores/reglas, población, labels observables, capacidad, baseline y outcomes → comparación de políticas de selección y límites de inferencia.
- **Check propuesto:** revisa evaluación fuera de muestra, empates, capacidad y sesgo de etiquetas; no extrapola desde inspeccionados a toda la población sin respaldo.
- **Escenarios:** C1, C4, C5, C14 y C19–C21; C17 cuando la política selecciona solicitudes bajo restricciones pertinentes. C23/C24 aportan límites específicos: targeting causal y selección sin labels requieren H23/H24, respectivamente.
- **Artefacto/límite:** posible skill o gate ampliado; su scope son acciones sobre casos bajo capacidad, con outputs medibles definidos.

## H06 — `forecast-backtesting`

- **Trigger/problema:** el desempeño de forecast se calcula con cortes, horizontes o información ajenos a la decisión real.
- **Inputs → output:** series, timestamps, horizonte, frecuencia, información disponible y decisión → plan de backtesting, baselines, métricas por horizonte y evaluación operacional.
- **Check propuesto:** evita información futura; revisa ventanas, picos, stockouts/backlog y agregaciones que esconden fallos.
- **Escenarios:** C2 y C12; usar unidades y costes distintos para estudiar portabilidad.
- **Artefacto/límite:** posible extensión acotada de `design-validation` o skill nueva, según los fallos observados; no duplica toda la validación supervisada.

## H07 — `evaluate-grounded-assistant`

- **Trigger/problema:** se declara útil un asistente documental basándose en respuestas plausibles o unos pocos ejemplos.
- **Inputs → output:** preguntas representativas, documentos autorizados, referencias esperadas y política de abstención → evaluación separada de retrieval, respuesta, permisos y escalamiento.
- **Check propuesto:** detecta afirmaciones sin respaldo, citas incompatibles, acceso indebido y abstención incorrecta con evidencia por caso.
- **Escenarios:** C6; falta una segunda variante de asistente para revisar transferibilidad.
- **Artefacto/límite:** posible skill de evaluación más eval set/gates; no valida automáticamente extracción estructurada ni acciones de herramientas.

## H08 — `synthesize-evidence-to-recommendation`

- **Trigger/problema:** findings correctos producen recomendaciones sin relación trazable con la decisión y sus límites.
- **Inputs → output:** claims, evidencia, alternativas, supuestos, restricciones y audiencia → recomendación condicionada, opciones, rationale y siguiente acción.
- **Check propuesto:** cada afirmación material tiene soporte y cada recomendación declara incertidumbre/condiciones; no añade cifras o claims al resumir.
- **Escenarios:** C1–C24; contrastar análisis técnico, auditoría, riesgo y research.
- **Artefacto/límite:** probar primero playbook/template de delivery; una skill tendría que aportar una mejora verificable a esa base.

## H09 — `reconcile-business-metrics`

- **Trigger/problema:** reportes difieren y no existe explicación reproducible de definiciones y transformaciones.
- **Inputs → output:** contratos, fuentes, SQL, reportes y cortes → definición comparada, linaje y puente que explica diferencias.
- **Check propuesto:** revisa grain, filtros, joins, timestamps, unidades y denominadores; concilia bajo igual definición o registra diferencia pendiente.
- **Escenarios:** C8, C15 y C18/C21 cuando divergen definiciones; C2/C12 como variantes con medición inconsistente.
- **Artefacto/límite:** template/gate primero; posible skill de diagnóstico si el procedimiento se repite. No elige una definición oficial sin owner.

## H10 — `design-entity-resolution`

- **Trigger/problema:** unir sistemas requiere decidir qué registros representan la misma entidad y con qué riesgos.
- **Inputs → output:** entidades, claves, atributos, historia y coste de falsos matches → estrategia de vínculos, evaluación, revisión y reversión.
- **Check propuesto:** detecta cardinalidades, identidades ambiguas y fusiones erróneas; evalúa una muestra revisada y conserva linaje.
- **Escenarios:** C9; C21 si la relación usuario/cuenta/contrato presenta problemas de identidad. Falta aún otra evaluación completa de resolución de entidades.
- **Artefacto/límite:** contrato/mapping primero; posible skill especializada. Comprender un dataset no valida automáticamente la resolución de identidad.

## H11 — `assess-decision-data-readiness`

- **Trigger/problema:** hay datasets disponibles pero no evidencia suficiente para sostener la decisión propuesta.
- **Inputs → output:** decisión, fuentes, definiciones, disponibilidad, población y problemas de calidad → matriz requisito/fuente, brechas, impacto y recomendación de alcance.
- **Check propuesto:** distingue presencia de datos de suficiencia para decidir; prioriza brechas y evita certificar readiness sin evidencia.
- **Escenarios:** C1–C5, C8–C15 y C17–C21. C22–C24; revisar costes, evidencia de asignación o referencia sin labels según la decisión.
- **Artefacto/límite:** revisar primero extensión de `understand-dataset` más gate/contrato; posible duplicidad alta, no proponer nueva skill sin contrastar.

## H12 — `evaluate-document-extraction`

- **Trigger/problema:** el output estructurado parece correcto, pero campos, formatos o documentos fallan al incorporarse al proceso.
- **Inputs → output:** schema, documentos, anotaciones, normalización y tolerancias → evaluación por campo/documento, fallos por formato y carga de revisión.
- **Check propuesto:** diferencia campos ausentes/incorrectos, conserva origen, separa desarrollo/evaluación y prueba formatos nuevos y documentos duplicados.
- **Escenarios:** C10; falta un segundo tipo documental antes de sostener generalidad.
- **Artefacto/límite:** schema/eval set primero; posible skill con ámbito propio. No equivale a evaluar respuestas libres con fuentes.

## H13 — `evaluate-recommendation-policy`

- **Trigger/problema:** una política de recomendación se selecciona por métricas offline incompatibles con exposición, usuarios nuevos o experiencia.
- **Inputs → output:** catálogo, exposures, interacción, política histórica y superficie → baselines, evaluación offline, límites y plan online.
- **Check propuesto:** identifica sesgo de exposición, temporalidad, cold start, stock y trade-offs; no interpreta ausencia de clic como rechazo observado universal.
- **Escenarios:** C11; falta una variante de recomendación distinta de productos.
- **Artefacto/límite:** posible skill especializada; mantener scope distinto de H05 o compartir componentes solo después de evaluar.

## H14 — `audit-inherited-solution`

- **Trigger/problema:** se cuestiona una solución existente cuyo contexto, versión o evidencia están incompletos.
- **Inputs → output:** propósito recuperado, contratos, código, datos, versiones y logs disponibles → inventario verificable, hallazgos, límites y remediación priorizada.
- **Check propuesto:** separa confirmado/no verificable y no obliga a reconstruir componentes para declarar una auditoría completa.
- **Escenarios:** C14; añadir en futuras simulaciones una solución heredada de otro tipo.
- **Artefacto/límite:** playbook de auditoría primero; posible skill de coordinación del diagnóstico. Usa skills existentes para checks técnicos concretos.

## H15 — `diagnose-event-log-process`

- **Trigger/problema:** se comparan tiempos o flujos sin aclarar qué caso/evento representa el sistema.
- **Inputs → output:** logs, semántica, owners y variantes → contrato de eventos, flujo, duraciones válidas y hipótesis de cuellos de botella.
- **Check propuesto:** detecta casos abiertos excluidos, timestamps incomparables y pasos no registrados antes de atribuir causas.
- **Escenarios:** C15; preparar una segunda variante de proceso con eventos diferentes.
- **Artefacto/límite:** template/playbook inicialmente; posible skill si el procedimiento especializado aporta valor frente al análisis de datos existente.

## H16 — `define-agent-action-boundaries`

- **Trigger/problema:** se propone delegar acciones a un agent sin un contrato verificable de autoridad y herramientas.
- **Inputs → output:** tareas, APIs, permisos y consecuencias → acciones permitidas/propuestas, approvals, contratos, escalamiento y escenarios de fallo.
- **Check propuesto:** simular reintentos, errores, contenido externo con instrucciones y acciones duplicadas; exigir evidencia de aprobación para cambios pertinentes.
- **Escenarios:** C16; requiere otra familia de herramientas para estudiar portabilidad.
- **Artefacto/límite:** contratos/gates primero; posible skill de diseño/revisión. Un agent reusable requiere candidate independiente con responsabilidades y autoridad.

## H17 — `design-operational-monitoring`

- **Trigger/problema:** la solución pasa un piloto pero carece de señales y responsables para detectar degradación en uso.
- **Inputs → output:** decisión, servicios, data contracts, fallos y owners → señales, umbrales justificados, frecuencia, respuesta y revisión.
- **Check propuesto:** cada alerta tiene señal disponible, owner y acción; distingue cambios de datos, sistema y resultados del negocio.
- **Escenarios:** C5, C6, C9–C12, C14, C16 y C17–C21 cuando la solución se usará operativamente. C22–C24 si las estimaciones/políticas/alertas pasan a operación.
- **Artefacto/límite:** playbook y runbook inicialmente; considerar skill solo si mejora el diseño recurrente. No ejecuta respuestas en producción automáticamente.

## H18 — `design-human-review-policy`

- **Trigger/problema:** la automatización deja excepciones sin criterio, capacidad o responsable de revisión.
- **Inputs → output:** errores tolerables, outcomes, capacidad de revisión, latencia y responsables → reglas de abstención, revisión, muestreo, escalamiento y trazabilidad.
- **Check propuesto:** calcula o declara carga de revisión y trade-offs usando inputs provistos; no asume confianza calibrada ni capacidad ilimitada.
- **Escenarios:** C4–C6, C9, C10, C14, C16 y C17/C19/C21 cuando la decisión necesita revisión humana. C24 para la cola de investigación; C22/C23 solo si hay decisiones que requieran revisión humana.
- **Artefacto/límite:** contrato/gate transversal primero; posible procedimiento reusable sin sustituir las validaciones específicas del sistema.

## H19 — `evaluate-probability-calibration`

- **Trigger/problema:** un score separa clases pero se interpreta como una probabilidad confiable sin evidencia.
- **Inputs → output:** predicciones fuera de muestra, outcomes maduros, población/horizonte y uso de la probabilidad → diagnóstico de calibración, incertidumbre y límites por período/segmento.
- **Check propuesto:** distingue discriminación y calibración, conserva un conjunto independiente para evaluar ajustes y no extrapola a poblaciones sin labels compatibles.
- **Escenarios:** C1, C4, C5, C17, C18, C20 y C21 cuando la decisión usa probabilidades.
- **Artefacto/límite:** posible skill o extensión de validación; un score, riesgo latente o probabilidad de retorno requiere una definición de outcome evaluable.

## H20 — `validate-delayed-outcome-targets`

- **Trigger/problema:** se tratan como negativos casos cuyo outcome todavía no pudo observarse durante el horizonte requerido.
- **Inputs → output:** evento, fechas, horizonte, ventanas, delays y criterios de etiqueta → contrato de target, cohortes elegibles, maduración y límites de observación.
- **Check propuesto:** diferencia negativo observado, outcome pendiente, censura y label ausente; verifica que el momento de predicción anteceda a los datos del outcome.
- **Escenarios:** C1, C4, C5 y C17–C21. C22/C23 para valor/outcomes cuyo horizonte aún no se completa; en C24 ausencia de labels no equivale a outcome pendiente.
- **Artefacto/límite:** gate/contrato temporal o extensión de `understand-dataset`/`design-validation` antes de justificar una skill nueva. No impone un único tratamiento estadístico de censura.

## H21 — `design-time-to-event-evaluation`

- **Trigger/problema:** la decisión necesita cuándo podría ocurrir un evento y la observación contiene censura o períodos de seguimiento distintos.
- **Inputs → output:** evento, origen temporal, entrada, seguimiento, censura y acciones → diseño de evaluación de tiempo hasta evento, baselines, horizontes y supuestos.
- **Check propuesto:** alinea población y tiempos de observación, evalúa con información disponible y declara supuestos sobre censura; no aplica supervivencia sin justificación.
- **Escenarios:** C5, C20 y C21 si la formulación elegida es de tiempo hasta evento. C22 únicamente si se modela tiempo hasta evento observable, no por usar CLV.
- **Artefacto/límite:** posible extensión especializada de validación; en churn no contractual la salida de la relación puede ser latente y exige revisar si la formulación/labels permiten esta evaluación.

## H22 — `estimate-customer-lifetime-value`

- **Trigger/problema:** ingresos históricos se presentan como valor futuro o se asigna inversión sin definir horizonte, contribución y población.
- **Inputs → output:** transacciones, márgenes/costes, cohortes, seguimiento, momento de decisión, horizonte y supuestos de descuento → contrato de valor, baseline, estimación residual/truncada y sensibilidad por cohorte.
- **Check propuesto:** compara predicción con valor observado al mismo horizonte en cohortes/períodos independientes; detecta seguimiento incompleto, doble conteo de costes y extrapolación a prospectos sin evidencia. No inventa márgenes ni tasas.
- **Escenarios:** C22; falta contrastar una variante contractual y otra decisión de adquisición para estudiar generalidad.
- **Artefacto/límite:** contrato/template primero y posible procedimiento especializado. H02 traduce valor a escenarios de impacto, H21 solo cubre tiempo hasta evento cuando aplica. Estimar CLV no identifica el efecto incremental de una campaña ni determina por sí solo el CAC máximo.

## H23 — `evaluate-uplift-targeting`

- **Trigger/problema:** se eligen destinatarios por propensión o subgrupos exploratorios y se afirma que son quienes más se benefician de una intervención.
- **Inputs → output:** tratamiento/control, asignación, covariables previas, outcomes maduros, identificación, costes, capacidad y política → diseño de evaluación independiente del valor causal de targeting, baselines, incertidumbre y límites de soporte.
- **Check propuesto:** detecta variables posteriores al tratamiento, ausencia de control/overlap y reutilización del conjunto de evaluación para elegir política; compara alternativas bajo restricciones comunes. No usa un supuesto efecto individual observado como ground truth ni declara certeza individual.
- **Escenarios:** C23; C22 si la retención se evalúa por efecto incremental. Añadir otra intervención antes de sostener transferibilidad.
- **Artefacto/límite:** contrastar extensión de H04/H05 frente a skill especializada. H04 diseña identificación/evaluación de la intervención; H23 evalúa política por heterogeneidad causal. No presupone que campañas históricas permiten identificar efectos.

## H24 — `design-unlabeled-anomaly-review`

- **Trigger/problema:** se evalúa detección sin labels con métricas supervisadas inventadas o se interpreta rareza como incidencia confirmada.
- **Inputs → output:** eventos/contexto, referencia temporal, acciones, capacidad de revisión y criterios expertos → plan de evaluación sin labels, cola/muestreo, feedback trazable y límites de inferencia.
- **Check propuesto:** separa cambio legítimo, error de datos y caso accionable; revisa estabilidad/carga y muestreo fuera del top. Anomalías sintéticas verifican patrones concretos sin acreditar precision/recall reales; feedback seleccionado requiere revisar sesgo antes de reentrenar.
- **Escenarios:** C24; añadir otra fuente de anomalías y otra organización de revisión antes de afirmar generalidad.
- **Artefacto/límite:** playbook/contrato inicialmente; posible skill de diseño de evaluación si supera la combinación H11/H17/H18. H18 fija revisión/autoridad y H17 monitoreo; H24 aborda evidencia y aprendizaje sin labels. No certifica fraude, crea un agent ni ejecuta bloqueos.

## Relaciones revisadas al documentar candidates; por contrastar antes de experimentar

- H01/H02/H08 se conectan, pero framing, estimación de impacto y síntesis tienen inputs y outputs diferentes. Evitar empaquetar el lifecycle entero como una skill.
- H06/H11/H14 pueden ampliar o coordinar capacidades existentes. Comparar primero con `understand-dataset`, `design-validation` y `detect-leakage`.
- H05/H13 comparten ordenamiento, pero selección operativa y recomendación con exposición tienen decisiones/evidencia distintas.
- H07/H12/H16 cubren respuestas, extracción y acciones. Puede compartirse una pauta de evaluación, conservando checks específicos.
- H17/H18 se repiten entre escenarios, pero pueden resolverse mediante playbooks, contratos y gates. Frecuencia simulada no determina su forma.
- H19/H20/H21 revisan probabilidad, observabilidad del target y tiempo hasta evento. Contrastar primero sus límites con las skills de datos/validación existentes; riesgo de crédito o churn no justifican una skill sectorial que duplique esos procedimientos.

- H22/H02/H21 separan estimación de valor, impacto de una decisión y tiempo hasta evento. CLV puede necesitar compras/márgenes además de supervivencia; no empaquetar todo como una skill sectorial.
- H23/H04/H05 separan identificación de intervención y evaluación de targeting causal. Examinar una extensión antes de duplicar procedimientos.
- H24/H11/H17/H18 separan evaluación sin labels, suficiencia de fuentes, monitoreo y revisión humana. La falta de labels no activa automáticamente ninguna skill supervisada.

## Próximas extensiones del análisis

Para contrastar las hipótesis con cobertura de un solo escenario, conviene añadir variantes de resolución de identidad, extracción de otro tipo documental, recomendación distinta de productos, auditoría heredada de un pipeline, otro proceso con event logs y un agent con herramientas diferentes. Variar también ausencia de datos, integraciones indisponibles, falta de labels y desacuerdo entre stakeholders.

Se conservarán IDs H01–H24 y se anotarán los nuevos escenarios y contradicciones. Las fichas se documentaron con el template canónico del Foundry. Una reapertura debe respetar la decisión y el trigger vigentes en cada ficha; si se propone pasar a experimental, completar evidencia, resolver el artefacto y revisar el candidate gate; este registro permanece como fuente exploratoria del proyecto ACOS.
