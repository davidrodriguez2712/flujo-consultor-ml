# Simulaciones de engagements para ACOS y oportunidades del Foundry

**Estado:** análisis hipotético para revisar el diseño  
**Fecha:** 4 de octubre de 2026  
**Base:** [spec aprobado del ACOS Project Compiler](../specs/2026-10-04-acos-project-compiler-design.md)

## Propósito y alcance

Estas simulaciones ponen a prueba la composición modular de ACOS con veinticuatro decisiones de negocio diferentes. Cada caso recorre discovery, framing, diagnóstico/evidencia, diseño/ejecución, validación, recomendación/delivery y handoff. Los datos, empresas y resultados son ficticios. Las repeticiones entre casos sirven para identificar **hipótesis** de capacidades; no demuestran recurrencia real ni validan una skill del Foundry.

El [registro acumulativo de hipótesis](2026-10-04-acos-candidate-hypotheses.md) conserva sus identificadores, triggers, inputs, outputs, límites y posibles casos de evaluación. El ejercicio sigue abierto: sus prioridades son provisionales y pueden cambiar al añadir escenarios. Las 24 hipótesis ya tienen [fichas candidate en el Foundry](2026-10-04-acos-foundry-candidate-map.md), con decisiones actualizadas: 18 se mantienen como conocimiento y seis quedan diferidas. La [revisión del 6 de octubre](2026-10-06-acos-foundry-integration.md) registra el inventario operativo y experimentos archivados.

El inventario operativo confirmado el 6 de octubre de 2026 contiene nueve skills en `experiments/skills/`, todas `experimental 0.1.0`. Ocho podrían apoyar trabajos de cliente bajo condiciones concretas. `run-skill-eval` sirve al proceso de evaluación del Foundry. La selección en un proyecto exige pertinencia y confirmación humana, según el spec.

| ID | Engagement hipotético | Arquetipos principales | Forma de entrega |
|---|---|---|---|
| C1 | Churn contractual y retención de suscripciones | `DIAGNOSE`, `PREDICT`, `EXPERIMENT_CAUSAL`, `RECOMMEND` | Política de contactos, piloto y memo |
| C2 | Demanda y abastecimiento de tiendas | `FORECAST`, `OPTIMIZE` | Plan de reposición/capacidad y análisis |
| C3 | Descuentos B2B | `DIAGNOSE`, `SEGMENT`, `EXPERIMENT_CAUSAL`, `OPTIMIZE` | Política de precios y piloto |
| C4 | Inspecciones por pérdidas de energía | `PREDICT`, `PRIORITIZE_SELECT`, `OPTIMIZE` | Priorización y plan operativo |
| C5 | Mantenimiento de maquinaria | `PREDICT`, `PRIORITIZE_SELECT` | Plan de inspecciones y monitoreo |
| C6 | Asistente interno de conocimiento | `RECOMMEND` y automatización | Producto GenAI con escalamiento humano |
| C7 | Entrada a un nuevo mercado | `DIAGNOSE`, `RECOMMEND` | Decision memo y executive deck |
| C8 | Dashboards con cifras contradictorias | `DIAGNOSE` | Contrato de métricas y reconciliación |
| C9 | Unificación de entidades entre sistemas | `DIAGNOSE` y automatización | Plan de integración y resolución de identidad |
| C10 | Extracción de facturas y documentos | Automatización documental | Pipeline, eval set y revisión humana |
| C11 | Recomendación de productos | `RECOMMEND`, `EXPERIMENT_CAUSAL` | Política de recomendaciones y piloto |
| C12 | Forecast y dotación de soporte | `FORECAST`, `OPTIMIZE` | Plan de turnos y capacidad |
| C13 | Piloto de una intervención en tiendas | `EXPERIMENT_CAUSAL` | Diseño experimental y decisión de expansión |
| C14 | Auditoría de un modelo heredado | `DIAGNOSE`, `PREDICT`, `PRIORITIZE_SELECT` | Informe de evaluación y plan de corrección |
| C15 | Cuellos de botella de pedidos | `DIAGNOSE`, `OPTIMIZE` | Mapa de proceso y plan de mejora |
| C16 | Agent que prepara acciones en CRM | Automatización y producto AI | Prototipo con contratos de herramientas y runbook |
| C17 | Riesgo de crédito en originación | `PREDICT`, `RECOMMEND` | Evaluación de riesgo y propuesta de política |
| C18 | Deterioro y monitoreo de cartera crediticia | `DIAGNOSE`, `PREDICT` | Análisis de cohortes, alertas y recomendaciones |
| C19 | Priorización de acciones de cobranza | `PRIORITIZE_SELECT`, `EXPERIMENT_CAUSAL`, `OPTIMIZE` | Política de contactos y piloto |
| C20 | Churn no contractual y reactivación | `DIAGNOSE`, `PREDICT`, `EXPERIMENT_CAUSAL` | Definición de inactividad y política de reactivación |
| C21 | Churn y renovación de cuentas B2B | `PREDICT`, `PRIORITIZE_SELECT` | Early warning y plan de seguimiento comercial |
| C22 | Customer Lifetime Value y presupuesto | `PREDICT`, `OPTIMIZE` | Estimación de valor y escenarios de inversión |
| C23 | Uplift de una intervención de retención | `EXPERIMENT_CAUSAL`, `PRIORITIZE_SELECT`, `OPTIMIZE` | Política de targeting y piloto |
| C24 | Anomalías sin labels en pagos | `DIAGNOSE`, `PRIORITIZE_SELECT` | Cola de revisión, evaluación y protocolo |

## C1. Churn contractual y retención de suscripciones

**Decisión:** a qué clientes contactar, con qué intervención y con qué límite de presupuesto. **Éxito:** margen incremental neto de la política de retención, con guardrails de experiencia de cliente. **Fuentes hipotéticas:** panel cliente-mes, bajas, campañas, contactos, costes e historial de producto.

**Recorrido E2E:**

1. Discovery: identificar quién decide la campaña, qué acciones puede ejecutar y qué tratamientos son permitidos.
2. Framing: fijar población, momento de decisión, capacidad de contacto, horizonte y métrica incremental.
3. Diagnóstico: comprender el panel, tasas base, cohortes y posible sesgo por campañas históricas.
4. Diseño/ejecución: construir un baseline de riesgo si añade valor y diseñar un piloto de intervenciones.
5. Validación: comprobar split temporal, leakage, cobertura de etiquetas y efecto causal del piloto; un score de churn no mide el efecto de una oferta.
6. Delivery: comparar política actual, política propuesta, costes y escenarios; recomendar el siguiente piloto o despliegue.
7. Handoff: documentar reglas de elegibilidad, responsables, medición y revisión de resultados.

**Skills actuales pertinentes:** `understand-dataset` para las fuentes nuevas; `design-validation` y `detect-leakage` si se elige una ruta supervisada con target y momento de decisión definidos; `build-features` solo si se diseña feature engineering. Todas requieren revisión de ajuste al caso.

**Brechas observadas:** framing de decisión y métricas, diseño de evaluación de intervención, estimación de impacto incremental y traducción de evidencia a política. El contrato de datos y el plan del piloto pueden empezar como templates/gates del OS.

## C2. Demanda y abastecimiento de tiendas

**Decisión:** cuánto reponer y qué capacidad asignar a cada tienda por período. **Éxito:** coste total de faltantes, exceso, desperdicio y capacidad, con restricciones de servicio. **Fuentes hipotéticas:** ventas diarias, stock, faltantes, promociones, calendario, plazos de proveedor y capacidad logística.

**Recorrido E2E:**

1. Discovery: precisar quién decide reposición, frecuencia de decisión y límites operativos.
2. Framing: definir horizonte, unidad tienda-producto, restricciones y función de coste.
3. Diagnóstico: comprobar si ventas observadas reflejan demanda cuando hubo faltantes y si promociones futuras son conocidas al decidir.
4. Diseño/ejecución: construir baseline de forecast y escenarios de asignación bajo capacidad.
5. Validación: ejecutar backtesting fuera de tiempo y comparar políticas completas, no solo error de forecast.
6. Delivery: presentar trade-offs de servicio, inventario, desperdicio y capacidad.
7. Handoff: dejar reglas de actualización, revisión de excepciones y monitoreo de error por segmento.

**Skills actuales pertinentes:** `understand-dataset`; `design-validation` y `detect-leakage` requieren revisión de fit para forecasting; `build-features` solo si se elige un modelo supervisado con variables derivadas.

**Brechas observadas:** backtesting de forecast orientado a decisiones y formulación de optimización. Diccionario de fuentes, restricciones y escenarios son buenos candidatos a templates y gates antes de crear una skill.

## C3. Descuentos B2B

**Decisión:** qué rangos de descuento ofrecer por tipo de oportunidad sin destruir margen. **Éxito:** contribución incremental, con guardrails de conversión y retención. **Fuentes hipotéticas:** propuestas, descuentos, negociaciones, costes, cierres y renovaciones.

**Recorrido E2E:**

1. Discovery: entender quién aprueba descuentos y qué excepciones comerciales existen.
2. Framing: definir unidad de decisión, límites de margen, segmentos y acciones factibles.
3. Diagnóstico: estudiar descuentos históricos y sesgo de negociación; un descuento observado se eligió bajo circunstancias particulares.
4. Diseño/ejecución: comparar reglas actuales, proponer bandas y diseñar un piloto controlado cuando sea viable.
5. Validación: comprobar que la evidencia no atribuya causalidad a correlaciones históricas y que el piloto mida efectos y guardrails.
6. Delivery: presentar escenarios de margen y conversión junto con incertidumbre y condiciones de aplicación.
7. Handoff: publicar reglas, aprobaciones, revisión de excepciones y mecanismo de seguimiento.

**Skills actuales pertinentes:** `understand-dataset`; `research-intelligence` solo si hay que comparar enfoques externos antes de elegir método. Las skills de ML supervisado no se activan por defecto.

**Brechas observadas:** diseño de evaluación causal, formulación de restricciones y cuantificación de impacto con supuestos explícitos. La política de aprobaciones pertenece al contrato de negocio y a un gate humano.

## C4. Inspecciones por pérdidas de energía

**Decisión:** qué suministros inspeccionar en el siguiente ciclo con capacidad limitada. **Éxito:** recupero neto por capacidad empleada, junto con restricciones operativas. **Fuentes hipotéticas:** consumos, suministros, inspecciones previas, resultados y disponibilidad de cuadrillas.

**Recorrido E2E:**

1. Discovery: comprender la selección actual y qué resultados de inspección se registran.
2. Framing: definir unidad suministro-período, momento de scoring, capacidad y objetivo operacional.
3. Diagnóstico: revisar cobertura temporal, duplicados, calidad y sesgo de etiquetas; los resultados pueden existir solo para suministros inspeccionados.
4. Diseño/ejecución: establecer baseline, estimar riesgo si es viable y construir una regla de selección bajo restricciones.
5. Validación: revisar leakage, split, sesgo de selección, calidad de priorización y factibilidad del plan; no afirmar rendimiento en toda la población usando solo etiquetas observadas en inspeccionados.
6. Delivery: comparar con la práctica actual y mostrar valor esperado bajo supuestos visibles.
7. Handoff: entregar criterios, revisión humana, registro de resultados y aprendizaje del siguiente ciclo.

**Skills actuales pertinentes:** `understand-dataset`, `design-validation`, `detect-leakage`; `build-features` solo antes de construir variables para un modelo supervisado. La coincidencia de dominio con el origen de algunas skills no sustituye su evaluación.

**Brechas observadas:** evaluación de una política de selección con etiquetas parciales, formulación de capacidad/ruteo e impacto operacional. El registro de supuestos y el gate de validez de etiquetas son artefactos previos a una posible skill.

## C5. Mantenimiento de maquinaria

**Decisión:** qué máquinas inspeccionar o detener preventivamente durante una ventana de mantenimiento. **Éxito:** tiempo de parada y coste evitado frente al coste de inspección y falsas alarmas. **Fuentes hipotéticas:** sensores, órdenes, fallos, ciclos de uso y ventanas de producción.

**Recorrido E2E:**

1. Discovery: entender frecuencia de inspección, capacidad técnica y consecuencias de una alerta.
2. Framing: definir horizonte de anticipación, unidad máquina-tiempo y acción factible.
3. Diagnóstico: revisar eventos, censura, mantenimiento preventivo anterior y disponibilidad real de sensores al decidir.
4. Diseño/ejecución: comparar reglas actuales con un baseline predictivo y una política de priorización.
5. Validación: probar separación temporal/por máquina, lead time útil, falsas alarmas y estabilidad entre equipos.
6. Delivery: recomendar umbrales o cupos con análisis de sensibilidad de costes.
7. Handoff: entregar protocolo de alertas, responsables y señales para recalibrar la política.

**Skills actuales pertinentes:** `understand-dataset`, `design-validation`, `detect-leakage`; `build-features` es condicional al enfoque de modelado elegido.

**Brechas observadas:** evaluación de selección bajo capacidad, traducción de scores a costes operativos y monitoreo de una política en uso. Los umbrales y reglas de escalamiento deben quedar como contrato operativo del proyecto.

## C6. Asistente interno de conocimiento

**Decisión:** qué preguntas puede responder el asistente con evidencia documental y cuándo debe escalar a una persona. **Éxito:** respuestas correctas y sustentadas, respeto de permisos, tiempo útil y tasa apropiada de escalamiento. **Fuentes hipotéticas:** documentación interna con niveles de acceso, historial de consultas y feedback de usuarios.

**Recorrido E2E:**

1. Discovery: identificar usuarios, tareas, restricciones de acceso y errores que no son aceptables.
2. Framing: definir alcance de preguntas, cuándo abstenerse y qué información puede mostrarse.
3. Diagnóstico: inventariar documentos, versiones, permisos y preguntas representativas.
4. Diseño/ejecución: diseñar retrieval, respuesta con referencias, escalamiento y una interfaz solo si la tarea la requiere.
5. Validación: comprobar calidad de retrieval, grounding, permisos, abstención, fallos y costes con casos separados del material de construcción.
6. Delivery: mostrar resultados y límites en un piloto con usuarios definidos.
7. Handoff: documentar actualización documental, evaluación recurrente, owner y manejo de incidentes.

**Skills actuales pertinentes:** `research-intelligence` para comparar enfoques cuando haga falta; `ui-planning` si se diseña una interacción nueva; `figma-handoff` si hay Figma/Design System/implementación; `visual-qa` si existe una UI ejecutable y referencia visual. Ninguna de ellas cubre por sí sola la evaluación de GenAI.

**Brechas observadas:** evaluación de respuestas y retrieval con evidencia, controles de acceso documental y política de abstención/escalamiento. Un contrato de fuentes, matriz de permisos y eval set pueden empezar como templates/gates.

## C7. Entrada a un nuevo mercado

**Decisión:** si entrar a uno de varios mercados y bajo qué condiciones. **Éxito:** decisión sustentada por atractivo, viabilidad, inversión, riesgos y umbrales de avance. **Fuentes hipotéticas:** entrevistas, documentos públicos, datos de mercado y estimaciones internas.

**Recorrido E2E:**

1. Discovery: identificar decisor, horizonte, apetito de riesgo y opciones reales.
2. Framing: definir criterios, umbrales y preguntas críticas antes de recopilar fuentes.
3. Diagnóstico: contrastar fuentes y separar hechos, inferencias y supuestos; registrar vacíos.
4. Diseño/ejecución: comparar escenarios de entrada y opciones de prueba limitada.
5. Validación: revisar procedencia, vigencia, contradicciones, sensibilidad y dependencia de supuestos.
6. Delivery: preparar decision memo y executive deck con recomendación condicionada.
7. Handoff: registrar señales a monitorear y decisiones que gatillan avance o abandono.

**Skills actuales pertinentes:** `research-intelligence`, si el alcance de sus fuentes y procedimiento se ajusta. No se seleccionan skills de dataset, modelado ni UI por defecto.

**Brechas observadas:** framing de decisión, business case con incertidumbre y síntesis de evidencia para recomendación. Un source register, matriz de escenarios y gate de calidad de evidencia ya pueden resolverse con playbook/template.

## C8. Dashboards con cifras contradictorias

**Decisión:** qué definición de ventas netas usar para gestionar el negocio y cómo corregir los reportes. **Éxito:** reconciliación explicada y reproducible entre fuentes y reportes. **Fuentes hipotéticas:** órdenes, pagos, devoluciones, cancelaciones, SQL y dashboards con distintas fechas de corte.

**Recorrido E2E:**

1. Discovery: identificar owners de fuentes/reportes y cómo se toman decisiones con las cifras.
2. Framing: acordar población, unidad, moneda, período, fecha de reconocimiento y tratamiento de devoluciones.
3. Diagnóstico: comparar filtros, grain, joins, duplicación, timestamps y transformaciones hasta localizar discrepancias.
4. Diseño/ejecución: construir un puente de reconciliación y un contrato de métricas con responsables.
5. Validación: explicar diferencias mediante casos trazables y conciliar totales bajo la misma definición y corte.
6. Delivery: presentar causas, cifras corregidas, límites y plan de reparación priorizado.
7. Handoff: documentar checks, ownership y cambios de definición que requieren aprobación.

**Skills actuales pertinentes:** `understand-dataset` para comprender tablas y relaciones. Una auditoría de reportes no activa por sí sola las skills de ML.

**Hipótesis:** H09 `reconcile-business-metrics`; H11 `assess-decision-data-readiness`, con posible solapamiento de esta última con `understand-dataset`. Contrato de métricas, SQL de reconciliación y gates pueden cubrir primero la necesidad.

## C9. Unificación de entidades entre sistemas

**Decisión:** cómo relacionar clientes, cuentas y contactos de CRM, facturación y soporte sin introducir asociaciones incorrectas. **Éxito:** cobertura y precisión de vínculos bajo tolerancias acordadas, con excepciones auditables. **Fuentes hipotéticas:** identificadores locales, atributos inconsistentes, registros duplicados e historial de cambios.

**Recorrido E2E:**

1. Discovery: conocer entidades, owners, accesos permitidos y consecuencias de unir registros incorrectos.
2. Framing: distinguir persona, cuenta y empresa; acordar qué representa un match y qué asociaciones requieren revisión.
3. Diagnóstico: estudiar claves, duplicados, cobertura, cardinalidades y cambios de identidad en el tiempo.
4. Diseño/ejecución: empezar por reglas deterministas, diseñar casos ambiguos y proponer matching adicional solo si hace falta.
5. Validación: evaluar falsos matches, no-matches y joins uno-a-varios con una muestra revisada y límites visibles.
6. Delivery: recomendar estrategia, tasas de revisión, límites de cobertura y migración gradual.
7. Handoff: entregar linaje, reglas de corrección/reversión y responsables de conflictos de identidad.

**Skills actuales pertinentes:** `understand-dataset`; `design-validation` y `detect-leakage` solo si se entrena o evalúa un componente supervisado de matching.

**Hipótesis:** H10 `design-entity-resolution`, H11 y H18 `design-human-review-policy`. Mapping de entidades y políticas de revisión/reversión pueden empezar como templates/gates; la complejidad de matching debe justificar una skill específica.

## C10. Extracción de facturas y documentos

**Decisión:** qué campos extraer automáticamente y qué documentos enviar a revisión. **Éxito:** exactitud por campo y documento, carga de revisión, latencia y coste bajo umbrales acordados. **Fuentes hipotéticas:** PDFs, imágenes, formatos variados y muestras revisadas por operadores.

**Recorrido E2E:**

1. Discovery: entender el proceso documental, tipos de error costosos y quién valida las excepciones.
2. Framing: definir schema de salida, campos obligatorios, tolerancias y criterios de abstención.
3. Diagnóstico: caracterizar formatos, calidad de imagen, duplicados y cobertura de la muestra anotada.
4. Diseño/ejecución: comparar reglas/OCR y extracción con AI según necesidad; mantener referencias al documento y campos de origen.
5. Validación: separar documentos de desarrollo/evaluación y comprobar campos, consistencia, errores por formato y carga real de revisión.
6. Delivery: presentar un piloto con ejemplos de fallos y escenarios de coste/calidad.
7. Handoff: documentar excepciones, actualización de formatos, revisión humana y monitoreo.

**Skills actuales pertinentes:** `understand-dataset` para anotaciones y tablas de evaluación, con alcance limitado a esos datos; skills UI solo si se necesita una interfaz nueva de revisión. Las skills actuales no cubren la evaluación documental completa.

**Hipótesis:** H12 `evaluate-document-extraction`, H18 y H17 `design-operational-monitoring`. El schema y los checks de consistencia son contratos/gates; la evaluación por campo/documento podría justificar una skill distinta de evaluar respuestas RAG.

## C11. Recomendación de productos

**Decisión:** qué productos mostrar en una superficie concreta y cómo comprobar que la política mejora el resultado. **Éxito:** resultado incremental acordado, con guardrails de diversidad, disponibilidad y experiencia. **Fuentes hipotéticas:** catálogo, exposición, clics, compras, stock y usuarios nuevos.

**Recorrido E2E:**

1. Discovery: precisar superficie, usuario, intención y reglas comerciales que limitan recomendaciones.
2. Framing: definir acción, unidad de exposición, métrica, cold start y baseline pertinente.
3. Diagnóstico: revisar logs de exposición, sesgo de la política histórica, disponibilidad y cobertura de usuarios/productos.
4. Diseño/ejecución: comparar popularidad/reglas con alternativas y preparar un piloto si el cambio es viable.
5. Validación: comprobar cortes temporales, evaluación offline y efecto online sin asumir que clics históricos describen preferencias completas.
6. Delivery: recomendar política, trade-offs, límites de interpretación y secuencia del piloto.
7. Handoff: dejar versionado de catálogo/política, monitoreo y gestión de productos nuevos o agotados.

**Skills actuales pertinentes:** `understand-dataset`; `design-validation`, `detect-leakage` y `build-features` si se usa una formulación supervisada compatible. `ui-planning` solo si cambia de forma importante la interacción.

**Hipótesis:** H13 `evaluate-recommendation-policy`, H04 `design-intervention-evaluation` y H17. H13 debe distinguirse de H05, que trata selección de casos para intervención bajo capacidad, para evitar un catálogo de skills que mezcle decisiones diferentes.

## C12. Forecast y dotación de soporte

**Decisión:** qué capacidad asignar por franja y canal de atención. **Éxito:** coste, espera, backlog y nivel de servicio bajo restricciones laborales/operativas provistas por el cliente. **Fuentes hipotéticas:** llegadas, duración, resoluciones, turnos, canales y campañas.

**Recorrido E2E:**

1. Discovery: entender canales, capacidad efectiva, habilidades de operadores y decisiones de turnos.
2. Framing: fijar horizontes, intervalos, métricas de servicio y restricciones concretas.
3. Diagnóstico: comprobar timestamps, llegadas versus tickets cerrados, backlog y variabilidad por canal.
4. Diseño/ejecución: comparar baselines de demanda/carga y simular alternativas de capacidad y turnos.
5. Validación: evaluar backtesting, picos y sensibilidad de servicio; un forecast preciso no garantiza una asignación operativa adecuada.
6. Delivery: presentar planes, escenarios de saturación y costes bajo supuestos declarados.
7. Handoff: dejar reglas de replanificación, alertas de capacidad y ownership de datos.

**Skills actuales pertinentes:** `understand-dataset`; `design-validation` y `detect-leakage` requieren revisión de alcance para la ruta de forecast; `build-features` solo con modelado supervisado.

**Hipótesis:** H06 `forecast-backtesting`, H03 `formulate-constrained-decision` y H17. Este caso da una segunda familia de forecast distinta de abastecimiento, útil para preparar evaluaciones de portabilidad.

## C13. Piloto de una intervención en tiendas

**Decisión:** si expandir un cambio de layout o promoción a más tiendas. **Éxito:** efecto incremental acordado, con guardrails de margen y operación. **Fuentes hipotéticas:** ventas por tienda-período, asignación al piloto, calendario y cumplimiento de la intervención.

**Recorrido E2E:**

1. Discovery: identificar cómo se implementa el cambio y qué unidades pueden asignarse a condiciones distintas.
2. Framing: definir estimand, población, unidad de asignación y medición, duración y regla de decisión.
3. Diagnóstico: revisar heterogeneidad entre tiendas, estacionalidad, contaminación y calidad del registro de implementación.
4. Diseño/ejecución: diseñar piloto considerando tiendas/grupos; si no se puede randomizar, explicitar límites y alternativas de identificación.
5. Validación: revisar cumplimiento, balance, precisión y guardrails usando un plan de análisis declarado previamente.
6. Delivery: recomendar expansión, repetición o ajuste con incertidumbre y condiciones de adopción.
7. Handoff: registrar decisiones, monitoreo del rollout y señales de reversión.

**Skills actuales pertinentes:** `understand-dataset` para las tablas del piloto. `design-validation` evalúa modelos supervisados y no sustituye diseño experimental.

**Hipótesis:** H04 y H02 `quantify-decision-impact`. El plan del piloto y el gate humano de expansión son artefactos necesarios aun cuando no se cree ninguna skill nueva.

## C14. Auditoría de un modelo heredado

**Decisión:** continuar usando, corregir o reemplazar una solución cuyo desempeño operativo se cuestiona. **Éxito:** diagnóstico verificable y decisión proporcional al riesgo y al valor de la solución. **Fuentes hipotéticas:** código, features, datasets de entrenamiento, predicciones, resultados y logs incompletos.

**Recorrido E2E:**

1. Discovery: recuperar la decisión original, owners, versión en uso y cambios del entorno.
2. Framing: definir preguntas de auditoría, alcance y criterios para mantener, limitar o corregir.
3. Diagnóstico: contrastar entrenamiento y producción, contratos, etiquetas, cohortes y linaje.
4. Diseño/ejecución: reconstruir evidencia disponible y comparar baseline, modelo y política operativa sin asumir reproducibilidad.
5. Validación: auditar leakage, split, disponibilidad de features y desempeño por período/segmento; declarar lo no verificable.
6. Delivery: recomendar corrección, uso limitado o retiro con evidencia y dependencias.
7. Handoff: dejar plan de remediación, monitoreo y responsables de aceptación.

**Skills actuales pertinentes:** `understand-dataset`, `detect-leakage` y `design-validation` según el objeto auditado. `build-features` se activa después, solo si se aprueba rediseñar variables.

**Hipótesis:** H14 `audit-inherited-solution`, H11 y H17. Este engagement entra operativamente en validación/auditoría; discovery y framing recuperan el contexto mínimo y no fuerzan reiniciar el proyecto completo.

## C15. Cuellos de botella de pedidos

**Decisión:** qué etapa del proceso de pedidos cambiar y cómo priorizar mejoras. **Éxito:** menor tiempo de ciclo y retrabajo, con guardrails de calidad. **Fuentes hipotéticas:** event logs de recepción, preparación, aprobación y entrega con eventos faltantes o tardíos.

**Recorrido E2E:**

1. Discovery: entrevistar operadores y owners para relacionar eventos del sistema con actividades reales.
2. Framing: definir caso, inicio/fin, unidades de tiempo, variantes y decisión de intervención.
3. Diagnóstico: revisar completitud, timestamps, duplicados, cambios de identificador y casos aún abiertos.
4. Diseño/ejecución: mapear flujo y variantes, tiempos de espera y retrabajo; contrastar cuellos de botella con responsables.
5. Validación: comprobar que las duraciones no se calculan únicamente sobre casos completados ni sobre eventos que el proceso no registra de forma comparable.
6. Delivery: recomendar cambios, piloto y medición de impacto bajo capacidad real.
7. Handoff: dejar definiciones, ownership de eventos y seguimiento de las mejoras.

**Skills actuales pertinentes:** `understand-dataset` para estructura/semántica inicial. No se activa modelado para identificar un cuello de botella descriptivo.

**Hipótesis:** H15 `diagnose-event-log-process`, H09 y H11. Mapa de proceso, contrato de eventos y gate de completitud pueden bastar antes de justificar una skill especializada.

## C16. Agent que prepara acciones en CRM

**Decisión:** qué tareas del flujo comercial delegar a un agent y qué acciones requieren aprobación. **Éxito:** tareas correctamente completadas, trazabilidad y carga de revisión razonable, con límites claros de escritura. **Fuentes hipotéticas:** contactos, notas, reglas de negocio, APIs y solicitudes de operadores.

**Recorrido E2E:**

1. Discovery: mapear tareas, herramientas, permisos y acciones externas que el proceso permite.
2. Framing: definir acciones permitidas, prohibidas y sujetas a aprobación; precisar cuándo escalar.
3. Diagnóstico: revisar APIs, contratos, datos incompletos y fallos de herramientas antes de elegir una arquitectura agentic.
4. Diseño/ejecución: comparar automatización determinista y agent; prototipar con herramientas simuladas y propuestas de acción revisables.
5. Validación: simular instrucciones ambiguas, contenido externo con instrucciones, fallos, reintentos y acciones duplicadas; comprobar límites y aprobación antes de ejecutar cambios.
6. Delivery: recomendar alcance de piloto y condiciones para habilitar cada acción.
7. Handoff: entregar contratos de herramientas, registro de acciones, responsables y procedimientos de pausa/reversión.

**Skills actuales pertinentes:** `research-intelligence` si se comparan enfoques y `ui-planning` si se necesita una interacción de revisión nueva. Las skills actuales de UI no validan autoridad ni ejecución de herramientas del agent.

**Hipótesis:** H16 `define-agent-action-boundaries`, H18 y H17. Los contratos de herramientas, gates de aprobación y límites del agent tienen prioridad. Crear un agent reutilizable requiere una responsabilidad propia y autoridad definida, además de evaluar su procedimiento.

## C17. Riesgo de crédito en originación

**Decisión:** qué solicitudes recomendar para aprobación, revisión o rechazo, bajo una política acordada por el owner de riesgo. **Éxito:** equilibrio explícito entre riesgo y objetivos comerciales, con restricciones, explicaciones y revisión pertinente. **Fuentes hipotéticas:** solicitudes históricas, decisiones, variables disponibles al solicitar y desempeño posterior de créditos otorgados.

**Recorrido E2E:**

1. Discovery: entender producto, política vigente, owner, datos permitidos y decisiones que el análisis puede apoyar.
2. Framing: acordar definición de incumplimiento, horizonte, fecha de scoring, población y criterios de aceptación.
3. Diagnóstico: revisar maduración de outcomes, cohortes y sesgo de selección: puede no existir desempeño observado para solicitudes rechazadas.
4. Diseño/ejecución: comparar baseline/modelo y escenarios de política, conservando separado score, probabilidad y decisión de aprobación.
5. Validación: comprobar discriminación, calibración, estabilidad temporal, segmentos, leakage y límites de extrapolación a rechazados.
6. Delivery: presentar resultados, restricciones y propuestas revisables; el owner decide la política.
7. Handoff: documentar versiones, monitoreo, overrides y condiciones de reevaluación.

**Skills actuales pertinentes:** `understand-dataset`, `design-validation`, `detect-leakage`; `build-features` solo para un modelo supervisado cuyo contrato temporal esté definido.

**Hipótesis:** H19 `evaluate-probability-calibration`, H20 `validate-delayed-outcome-targets`, H01/H05/H11/H17/H18. Calibración y discriminación deben tratarse como tareas distintas; esta distinción está desarrollada en [BIS: validación de sistemas de rating](https://www.bis.org/publications/studies-validation-internal-rating-systems-revised). La referencia es metodológica; la simulación no establece requisitos regulatorios de un país.

## C18. Deterioro y monitoreo de cartera crediticia

**Decisión:** qué cohortes o segmentos investigar y qué señales requieren revisión del equipo de riesgo. **Éxito:** alertas sustentadas que distingan cambios de población, maduración, definiciones y riesgo. **Fuentes hipotéticas:** cartera por período, pagos, atraso, reestructuraciones, scores y versiones de política.

**Recorrido E2E:**

1. Discovery: acordar usuarios del monitoreo, acciones factibles y frecuencia de decisiones.
2. Framing: definir cohortes/vintages, población, métricas y tratamiento de créditos con poca historia.
3. Diagnóstico: conciliar exposición, estados y denominadores; estudiar mix, maduración y cambios de política.
4. Diseño/ejecución: comparar tendencias y expectativas de riesgo con segmentación y escenarios documentados.
5. Validación: usar cohortes comparables y outcomes disponibles; evitar comparar directamente historias de observación distintas.
6. Delivery: recomendar investigación o ajustes con incertidumbre y límites de atribución.
7. Handoff: entregar definiciones, trazabilidad, owners y revisión de alertas.

**Skills actuales pertinentes:** `understand-dataset`; `design-validation`/`detect-leakage` cuando se evalúan componentes supervisados. Un reporte de cartera no exige entrenar un modelo.

**Hipótesis:** H09/H11/H17/H19/H20; pueden combinarse contratos de métricas y gates de maduración antes de crear una skill sectorial amplia.

## C19. Priorización de acciones de cobranza

**Decisión:** qué cuentas contactar, por qué canal y cuándo, bajo capacidad y políticas de contacto provistas por el cliente. **Éxito:** recuperación incremental neta y resultados de cliente bajo guardrails acordados. **Fuentes hipotéticas:** atraso, pagos, campañas, contactos, outcomes y costes.

**Recorrido E2E:**

1. Discovery: mapear acciones permitidas, capacidad, owners y registros de tratamientos históricos.
2. Framing: definir unidad, momento de decisión, acción, horizonte y resultado incremental.
3. Diagnóstico: distinguir pagos espontáneos, contactos históricos y cobertura sesgada de outcomes.
4. Diseño/ejecución: comparar regla vigente con políticas alternativas y diseñar un piloto de acciones cuando sea viable.
5. Validación: revisar temporalidad, selección, costes y efecto de la intervención; probabilidad de pago no equivale a beneficio del contacto.
6. Delivery: presentar escenarios de capacidad, recuperación y carga de revisión sin inventar valor económico.
7. Handoff: documentar controles, monitoreo, responsables y actualización de la política.

**Skills actuales pertinentes:** `understand-dataset`; skills supervisadas si se elige un modelo compatible. `design-validation` no sustituye el diseño causal del piloto.

**Hipótesis:** H02/H03/H04/H05/H18/H20. Las restricciones de contacto se reciben del cliente y se verifican en el engagement; este caso no prescribe reglas legales.

## C20. Churn no contractual y reactivación

**Decisión:** qué compradores probablemente inactivos deberían recibir una acción de reactivación. **Éxito:** actividad o margen incremental bajo presupuesto y experiencia acordados. **Fuentes hipotéticas:** compras, visitas, campañas, recencia, frecuencia y estacionalidad, sin evento formal de cancelación.

**Recorrido E2E:**

1. Discovery: comprender ciclos de recompra y cómo el negocio define una relación activa.
2. Framing: acordar qué inactividad se puede observar y qué es una hipótesis de abandono.
3. Diagnóstico: revisar patrones de compra, ventanas de observación, estacionalidad y observaciones censuradas.
4. Diseño/ejecución: comparar reglas de inactividad con enfoques de retorno o tiempo hasta evento, sin imponer un algoritmo.
5. Validación: comprobar horizontes, outcomes, calibración y sensibilidad a ventanas; evaluar el efecto de reactivación por separado.
6. Delivery: recomendar definición operativa, población y piloto con límites de interpretación.
7. Handoff: dejar revisión de ventanas, medición de retorno y seguimiento de campañas.

**Skills actuales pertinentes:** `understand-dataset`; skills supervisadas solo si la formulación y labels son compatibles.

**Hipótesis:** H04/H05/H19/H20/H21 `design-time-to-event-evaluation`. En contextos no contractuales, una pausa entre compras puede confundirse con abandono; este problema se describe en [Fader, Hardie y Shang: análisis de clientes no contractuales](https://www.brucehardie.com/papers/020/).

## C21. Churn y renovación de cuentas B2B

**Decisión:** qué cuentas requieren seguimiento antes de renovar y qué acciones comerciales son viables. **Éxito:** resultados de renovación y retención de ingresos con costes y guardrails acordados. **Fuentes hipotéticas:** contratos, renovaciones, uso por usuario/cuenta, incidencias, conversaciones y cambios de producto.

**Recorrido E2E:**

1. Discovery: entender ciclos de renovación, owner de cuenta y opciones reales de intervención.
2. Framing: separar churn de cuenta, caída de ingresos, downgrade y no renovación; fijar fecha de decisión y horizonte.
3. Diagnóstico: resolver granularidad cuenta/usuario, ventanas previas a renovación, labels maduros y causas conocidas.
4. Diseño/ejecución: comparar reglas de early warning y modelos si aportan valor; proponer un protocolo de seguimiento.
5. Validación: evaluar cortes por tiempo/cuenta y excluir información posterior a la decisión, como notas de cancelación tardías.
6. Delivery: presentar cobertura, incertidumbre, carga del equipo y recomendaciones para un piloto.
7. Handoff: documentar responsables de cuentas, outcomes y seguimiento de intervenciones.

**Skills actuales pertinentes:** `understand-dataset`, `design-validation`, `detect-leakage`; `build-features` solo en el diseño supervisado. Se revisa fit de cada una para granularidad y temporalidad B2B.

**Hipótesis:** H01/H04/H05/H09/H10/H19/H20/H21. El modelo identifica riesgo; el efecto de la acción comercial requiere su propia evidencia.

## C22. Customer Lifetime Value y presupuesto de adquisición/retención

**Decisión:** cuánto invertir por canal/cohorte de adquisición y qué presupuesto de retención justificar con evidencia incremental. **Éxito:** contribución esperada neta del gasto comercial, con límites de presupuesto y plazo de recuperación. **Fuentes hipotéticas:** transacciones de un ecommerce, devoluciones, márgenes, costes de servicio, fecha/canal de adquisición, campañas y seguimiento por cliente.

**Recorrido E2E:**

1. Discovery: separar clientes existentes de prospectos y decisiones de captación de decisiones de retención; acordar quién aprueba inversión y qué costes se observan.
2. Framing: definir valor residual desde el momento de decisión, margen/contribución, horizonte, descuento y tratamiento de costes de adquisición. Si se usa horizonte finito, explicitar CLV truncado y valor posterior no estimado; no inventar tasa de descuento ni restar dos veces el CAC.
3. Diagnóstico: revisar cohortes, estacionalidad, devoluciones, identidad, cobertura de márgenes y seguimiento desigual. La ausencia reciente de compra no demuestra abandono definitivo en una relación no contractual.
4. Diseño/ejecución: comparar baseline de contribución por cohorte con estimación de compras y valor futuro, si los datos lo permiten; formular escenarios de presupuesto y sensibilidad. Para prospectos, usar información disponible antes de adquirirlos y declarar incertidumbre al extrapolar desde clientes adquiridos.
5. Validación: reservar cohortes/períodos posteriores para comparar valor predicho y contribución observada en el mismo horizonte; separar seguimiento incompleto de valor cero. Evaluar errores por canal/cohorte y sensibilidad de asignación; el CLV esperado bajo la política actual no identifica cuánto añade una oferta de retención.
6. Delivery: entregar estimaciones con horizonte y supuestos, rangos de inversión y escenarios de CAC/payback. Condicionar aumentos de adquisición a respuesta marginal del canal y retención a evidencia causal o piloto; no fijar un presupuesto máximo universal igual al CLV promedio.
7. Handoff: documentar actualización de costes/cohortes, seguimiento de valor realizado, límites de extrapolación y revisión del presupuesto por el owner.

**Skills actuales pertinentes:** `understand-dataset`; `design-validation`, `detect-leakage` y `build-features` solo si se elige una formulación supervisada compatible. `research-intelligence` si hay que comparar modelos de compra, valor o supervivencia. Las skills actuales no cubren por sí solas CLV ni asignación causal de inversión.

**Hipótesis:** H01/H02/H03/H11/H20/H22; H17 cuando pase a operación, H04/H23 cuando se evalúe retención incremental y H21 si se elige tiempo hasta evento observable. H22 separa estimación de valor de la traducción a impacto H02. Costes, horizonte y descuento pueden empezar como contrato/template.

**Referencia de método:** la distinción entre valor esperado, horizonte truncado y valor residual se apoya en [Fader y Hardie: revisión de la fórmula de CLV](https://www.brucehardie.com/notes/033/what_is_wrong_with_this_CLV_formula.pdf). La composición del engagement es una hipótesis de ACOS.

## C23. Uplift para asignar una intervención de retención

**Decisión:** a quién ofrecer un incentivo para aumentar margen incremental con capacidad y presupuesto limitados. **Éxito:** valor incremental neto de la política frente a no intervenir y frente a la política actual, con guardrails de experiencia. **Fuentes hipotéticas:** piloto aleatorizado cliente a cliente, asignación treatment/control, oferta recibida, variables anteriores a la asignación, compras, margen y coste de incentivos/contactos.

**Recorrido E2E:**

1. Discovery: aclarar intervención, alternativa de control, elegibilidad, autoridad y si se conserva la asignación original del piloto; precisar si se busca efecto de asignar la oferta o de recibirla.
2. Framing: definir outcome/horizonte, estimand, unidad de asignación, costes, capacidad y población de aplicación. Separar probabilidad de comprar del cambio esperado causado por la oferta.
3. Diagnóstico: revisar aleatorización, pérdidas de seguimiento, cumplimiento, contaminación entre grupos y cobertura de segmentos. Si solo hay datos observacionales, exigir una estrategia de identificación y supuestos explícitos antes de interpretar diferencias como efectos.
4. Diseño/ejecución: comparar no intervenir, intervenir a todos los elegibles y una política simple bajo igual presupuesto; entrenar una política de targeting con información previa al tratamiento y reservar evaluación independiente. Buscar heterogeneidad sin convertir subgrupos exploratorios en resultados confirmados.
5. Validación: estimar valor de la política en datos independientes con treatment/control y soporte suficiente; revisar incertidumbre, costes, capacidad y sensibilidad por segmento. No calcular error individual contra un uplift verdadero observado: para una persona solo se observa un outcome bajo una asignación. Las curvas de uplift no sustituyen evaluar el objetivo económico y las condiciones causales.
6. Delivery: recomendar targeting, nuevo experimento o mantener la política simple según evidencia y precisión; presentar grupos sin evidencia suficiente y posibles efectos negativos, sin afirmar quién se beneficiará con certeza individual.
7. Handoff: entregar reglas reproducibles de elegibilidad/asignación, logging del piloto, revisión de costes y seguimiento controlado de la política antes de ampliar alcance.

**Skills actuales pertinentes:** `understand-dataset`; `research-intelligence` si se comparan métodos de estimación/policy learning. `design-validation` no sustituye evaluación causal. `detect-leakage`/`build-features` solo apoyan un componente supervisado compatible tras revisar fit; no certifican identificación ni uplift por sí solas.

**Hipótesis:** H01/H02/H03/H04/H05/H11/H20/H23; H17 si pasa a operación. H04 diseña la intervención/evidencia; H23 evalúa targeting por efecto heterogéneo y valor causal de la política. Antes de crear otra skill, contrastar si una extensión especializada de H04/H05 cubre la brecha.

**Referencia de método:** [Athey y Wager: Policy Learning with Observational Data](https://arxiv.org/abs/1702.02896) estudia políticas de tratamiento sujetas a restricciones bajo estrategias de identificación causal. No convierte cualquier registro de campañas en evidencia causal; la selección de módulos aquí es una hipótesis de diseño.

## C24. Anomalías sin labels en operaciones de pagos

**Decisión:** qué transacciones o patrones nuevos enviar a revisión y cuándo escalar una incidencia con capacidad limitada. **Éxito:** hallazgos accionables y tiempo de detección bajo carga de revisión sostenible; la precisión sobre toda la población permanece desconocida sin evidencia etiquetada adecuada. **Fuentes hipotéticas:** eventos de pagos, importes, timestamps, terminales, comercios, errores, cambios operativos y notas posteriores de analistas; no hay labels históricos confiables de anomalía/fraude.

**Recorrido E2E:**

1. Discovery: definir qué desviaciones interesan al equipo y qué acción puede seguir a una alerta; distinguir errores de datos, cambios legítimos y casos que requieren investigación.
2. Framing: fijar entidad/ventana, contexto de referencia, capacidad y latencia de revisión; un score de anomalía no es probabilidad de fraude ni motivo suficiente para bloquear pagos automáticamente.
3. Diagnóstico: inspeccionar calidad, cobertura, estacionalidad, segmentos y cambios de sistema. Revisar contaminación del conjunto de referencia y disponibilidad temporal de señales sin imponer un target supervisado inexistente.
4. Diseño/ejecución: comparar reglas/contextos simples con detectores no supervisados cuando aporten valor; conservar score, versión, contexto y razones disponibles. Diseñar cola y muestreo de revisión que incluya casos fuera del top de alertas para aprender sobre puntos ciegos.
5. Validación: comprobar estabilidad y volumen por período/segmento, reproducibilidad y carga operacional; usar revisión experta con criterios documentados y registrar desacuerdos. Casos conocidos o anomalías inyectadas comprueban sensibilidad a patrones concretos, pero no prueban precision/recall reales. El feedback seleccionado por la cola no representa automáticamente toda la población.
6. Delivery: entregar un piloto en modo observación, comparación con reglas y protocolo de investigación; explicitar qué calidad puede estimarse en la muestra revisada y qué queda desconocido.
7. Handoff: asignar owners, escalamiento, actualización de referencia y registro de resultados; ante cambios de régimen, revisar umbrales/contexto. Si se acumulan labels útiles, evaluar como cambio de alcance una ruta supervisada sin entrenar con feedback sesgado sin revisión.

**Skills actuales pertinentes:** `understand-dataset`; `research-intelligence` solo para comparar enfoques con una pregunta definida. Las skills supervisadas no se seleccionan por defecto por tratarse de ML. UI/`ui-planning` solo si se encarga una interacción de revisión nueva; una cola en herramientas existentes puede bastar.

**Hipótesis:** H01/H03/H11/H17/H18/H24; H02 si existe evidencia suficiente de coste/valor operacional. H24 diseña evaluación y aprendizaje sin labels, mientras H18 fija capacidad/autoridad de revisión y H17 monitoreo. No se propone un agent por necesitar una cola de casos.

**Referencia de método:** [Goix: evaluación de detección de anomalías sin supervisión](https://arxiv.org/abs/1607.01152) propone criterios sin labels como EM/MV y expone límites de estimación en alta dimensión. Estos criterios pueden apoyar comparación técnica bajo sus supuestos; no certifican la utilidad de las alertas para el negocio.

## Cobertura del Foundry actual

| Skill experimental | Casos donde podría proponerse | Límite de selección |
|---|---|---|
| `understand-dataset` | C1–C5, C8–C15 | Para datasets nuevos; en C10 cubre tablas/anotaciones, no toda la evaluación de documentos. |
| `design-validation` | C1, C4, C5, C9, C11, C14 con formulación supervisada; C2/C12 con revisión de alcance | No sustituye diseño experimental; forecasting y recomendación requieren revisar fit. |
| `detect-leakage` | C1, C4, C5, C14; C2/C9/C11/C12 si la tarea/pipeline es compatible | Requiere target, momento de decisión y pipeline pertinentes. |
| `build-features` | C1/C2/C4/C5/C11/C12 si se usa ML supervisado | En C9/C14 solo después de aprobar un rediseño supervisado; no se invoca por recibir datos. |
| `research-intelligence` | C7; C3/C6/C16 si se compara espacio de soluciones | Requiere pregunta de investigación y fuentes accesibles. |
| `ui-planning` | C6/C10/C11/C16 condicional | Solo si se crea o cambia significativamente una interacción de usuario. |
| `figma-handoff` | C6/C10/C11/C16 condicional | Requiere Figma, Design System y repositorio inspeccionable. |
| `visual-qa` | C6/C10/C11/C16 condicional | Requiere UI ejecutable y herramientas/referencia visual. |
| `run-skill-eval` | Ningún proyecto de cliente por defecto | Sirve a evaluaciones dentro del Foundry. |

En C17–C21 se propone `understand-dataset` para las fuentes nuevas. `design-validation`, `detect-leakage` y `build-features` se seleccionan únicamente si la ruta supervisada cumple sus condiciones. No se asume que estas skills cubren calibración, maduración de labels, análisis de supervivencia o causalidad completos.

En C22/C23 las skills supervisadas solo apoyan componentes compatibles; no cubren CLV o evaluación causal completos. En C24 se propone `understand-dataset` y, si procede, `research-intelligence`; no se incluyen skills supervisadas por defecto. Diseño/UI sigue condicionado a una interacción encargada y a los requisitos del stack/herramientas.

Esta matriz es una **propuesta de selección**, no una evaluación de eficacia. El resolver debe inspeccionar la versión, precondiciones y estado actuales al inicializar cada proyecto.

## Composición del workspace por escenario

El núcleo común definido en el spec se conserva en todos los casos. La tabla muestra áreas de trabajo adicionales, sujetas a la composición confirmada; los nombres no obligan a crear carpetas vacías.

| Caso | Áreas de trabajo pertinentes | Condiciones que cambian la composición |
|---|---|---|
| C1 | Datos, análisis, evaluación de intervenciones, decisión y delivery | Modelado solo si aporta valor; software/UI solo si se contrata una interacción o automatización. |
| C2 | Datos, forecast, escenarios, optimización, validación y handoff operativo | Puede empezar con un baseline simple; no necesita producto/UI para entregar un plan de reposición. |
| C3 | Datos, análisis, escenarios de precios, piloto, decisión y delivery | ML solo si se justifica; evaluación causal sigue siendo necesaria para afirmar efectos de descuentos. |
| C4 | Datos, análisis, priorización, validación y plan operativo | Modelado, optimización y ruteo dependen de viabilidad de etiquetas, capacidad y datos geográficos. |
| C5 | Datos, análisis, evaluación de políticas y monitoreo | Modelado depende de señales y etiquetas; serving/deployment solo si se acuerda operación del sistema. |
| C6 | Fuentes documentales, arquitectura, retrieval, evals, escalamiento y runbook | Producto/UI y sus skills se activan por una tarea de usuario real; el patrón RAG se confirma durante el diseño. |
| C7 | Research, evidencia, escenarios, recomendaciones, deck/memo y handoff | Sin datos tabulares, no se generan módulos de dataset, ML ni UI. |
| C8 | Definiciones, datos, SQL, reconciliación y decisiones | El engagement puede cerrar con contratos/checks y correcciones propuestas, sin construir una plataforma nueva. |
| C9 | Datos, mapping, integración, evaluación de matches y migración | Matching ML es opcional; la reversibilidad y ownership son requisitos del plan operativo. |
| C10 | Documentos, schemas, extracción, evals y revisión humana | OCR/reglas pueden bastar; UI solo si requiere una herramienta de revisión nueva. |
| C11 | Catálogo, análisis, política, evaluación y piloto | Recomendación puede usar reglas; una superficie existente puede recibir la política sin rediseño de UI. |
| C12 | Datos, forecast, simulación de capacidad, turnos y monitoreo | La dotación depende de carga y restricciones, además de volumen esperado. |
| C13 | Diseño experimental, datos, análisis, evidencia y rollout | No se compilan módulos ML por ejecutar un piloto. |
| C14 | Inventario heredado, auditoría, validación y remediación | Empieza en evaluación; conserva evidencia histórica y solo crea módulos de reconstrucción si se aprueban. |
| C15 | Eventos, análisis de proceso, variantes, mejoras y medición | No exige ML ni software nuevo para producir recomendaciones operativas. |
| C16 | Contratos de herramientas, prototipo, evals, aprobaciones y runbook | Un workflow determinista puede reemplazar la propuesta agentic; acciones externas dependen de autoridad explícita. |
| C17 | Datos, definición de target, modelado, validación y escenarios de política | Label maturity, selección y calibración condicionan viabilidad; política requiere owner. |
| C18 | Cartera, métricas, cohortes, monitoreo y decision memo | Puede cerrar con diagnóstico/alertas sin entrenar un modelo nuevo. |
| C19 | Datos, política de contactos, evaluación causal y escenarios de capacidad | Riesgo o propensión de pago no prueban el efecto de contactar. |
| C20 | Datos, definición de inactividad, evaluación temporal y piloto | Abandono puede ser no observado; supervivencia es una ruta posible, no obligatoria. |
| C21 | Contratos/cuentas, uso, early warning, evaluación y protocolo de seguimiento | Granularidad y calendario de renovación condicionan targets y splits. |
| C22 | Cohortes, costes, estimación de valor, validación y escenarios de inversión | Modelado depende de datos; experimento solo si se evalúa respuesta causal a inversión. |
| C23 | Asignación, outcomes, diseño causal, targeting, evaluación de política y piloto | Sin identificación/soporte no se habilita targeting causal; no exige UI nueva. |
| C24 | Eventos, referencia, detectores, revisión, feedback y monitoreo | No se genera validación supervisada sin labels; UI solo si cambia la interacción. |

## Ramas de fallo y cambio de alcance

Cada fila simula un hallazgo que cambia el recorrido. Son respuestas esperadas del flujo, pendientes de contrastar con ejecuciones futuras.

| Caso | Hallazgo hipotético | Resultado del gate y siguiente acción |
|---|---|---|
| C1 | Solo hay score de churn y faltan resultados de intervenciones | Limitar conclusión a riesgo; proponer piloto antes de afirmar impacto incremental. |
| C2 | Faltan registros de quiebres de stock | Separar ventas de demanda y declarar límites; mejorar captura o comparar escenarios. |
| C3 | Los mejores descuentos se dieron a oportunidades difíciles | Tratar sesgo de selección; evaluar piloto o estrategia causal antes de recomendar efecto. |
| C4 | Solo se conocen labels de suministros inspeccionados | Acotar evaluación a lo observable y diseñar un muestreo/piloto que permita ampliar evidencia. |
| C5 | Sensores predictivos llegan después del momento de decisión | Retirar esa información de la política y reevaluar viabilidad/lead time. |
| C6 | Retrieval muestra contenido fuera del permiso del usuario | Bloquear ese caso de uso y corregir controles antes del piloto. |
| C7 | La recomendación depende de una fuente sin respaldo | Condicionar o posponer la decisión y solicitar evidencia para ese supuesto. |
| C8 | Los dashboards usan fechas y reglas de devolución distintas | Aprobar definición común y puente de reconciliación; no imponer un total como verdad sin explicarlo. |
| C9 | Un contacto representa varias cuentas | Ajustar modelo de entidades/cardinalidad; revisar asociaciones antes de fusionarlas. |
| C10 | Un formato nuevo produce valores plausibles pero incorrectos | Derivar a revisión y ampliar eval set; no inferir exactitud por apariencia del output. |
| C11 | No se registraron exposiciones de productos | Acotar evaluación offline y mejorar logging; no atribuir preferencias a todos los productos no clicados. |
| C12 | El forecast medio funciona, pero los picos saturan soporte | Revisar capacidad y sensibilidad de servicio por franja; evitar aprobar solo por error agregado. |
| C13 | La intervención se comparte entre treatment y control | Replantear unidad/asignación o declarar límites de identificación. |
| C14 | No se puede reconstruir la versión que produjo los scores | Reportar evidencia insuficiente y definir remediación; no presentar una auditoría completa. |
| C15 | Los tickets abiertos desaparecen de la extracción | Corregir población antes de comparar tiempos y cuellos de botella. |
| C16 | Un reintento intenta duplicar una acción de escritura | Detener/escalar y comprobar idempotencia y aprobación antes de habilitar esa herramienta. |
| C17 | Los créditos recientes se etiquetaron como buenos sin completar el horizonte | Corregir maduración de labels y reevaluar; no aprobar métricas sobre negativos prematuros. |
| C18 | Una cohorte nueva se compara con otra que tuvo más meses de observación | Alinear maduración/denominadores antes de atribuir deterioro de riesgo. |
| C19 | La mayoría de pagos hubiera ocurrido sin contacto | Diseñar evaluación de intervención y comparar recuperación incremental. |
| C20 | Clientes estacionales se etiquetan como abandonados por una ventana fija | Revisar definición y sensibilidad; medir retorno sin fingir bajas observadas. |
| C21 | El registro de cancelación aparece después de la fecha de scoring | Excluir esa información, auditar construcción de variables y reevaluar el modelo. |
| C22 | Hay ingresos, pero faltan márgenes/costes y seguimiento de cohortes recientes | Reportar valor de ingresos al horizonte disponible; no afirmar CLV de contribución ni justificar gasto neto sin inputs. |
| C23 | Solo se registran clientes tratados y falta una comparación causal defendible | Bloquear conclusiones de uplift; recuperar asignación/control o diseñar nuevo piloto y acotar análisis a lo observable. |
| C24 | Un cambio legítimo de procesador genera muchas alertas | Revisar contexto/referencia y carga; investigar el cambio antes de interpretar rareza como fraude o bloquear operaciones. |

## Condiciones de portabilidad encontradas

Las skills consultadas de datos, research y UI describen rutas de reporte `reports/...` y también permiten una ruta indicada por el usuario. El contrato de tarea del proyecto debe indicar esa ruta explícitamente para que el output llegue al área compilada correspondiente. Esta adaptación se realiza mediante inputs e instrucciones de proyecto, conservando el contenido y hash del snapshot.

Además, varias skills incluyen referencias a documentos del Foundry, como su `AGENTS.md`, candidates o skills hermanas. La revisión de cobertura debe distinguir referencias de procedencia de dependencias necesarias para ejecutar. Una dependencia obligatoria no incluida en el snapshot se registra como limitación o brecha antes de confirmar la selección.

Para los escenarios con UI condicional, `figma-handoff` describe React/shadcn y `visual-qa` requiere Orca Browser/Design Mode. Un proyecto con otro stack o sin Orca no queda cubierto por copiar esos archivos: necesita una alternativa documentada o una adaptación evaluada en el Foundry.

## Oportunidades de capacidades nuevas

Los nombres siguientes corresponden a hipótesis documentadas como candidates, no a skills creadas ni experimentos aceptados. La cobertura indicada cuenta casos **simulados**; debe contrastarse con observaciones reales y el candidate gate del Foundry.

| ID | Hipótesis | Escenarios donde aparece | Tratamiento inicial |
|---|---|---|---|
| H01 | `frame-business-decision` | C1–C24 | Brief/gate; estudiar mejora frente al OS actual. |
| H02 | `quantify-decision-impact` | C1–C7, C10–C13, C15/C16, C19–C23; C17/C18/C24 con inputs suficientes | Playbook de impacto y escenarios; no forzar ROI cuando no es el objetivo. |
| H03 | `formulate-constrained-decision` | C2–C5, C12, C15, C19, C22–C24 con restricciones | Template de objetivos/restricciones; posible procedimiento reusable. |
| H04 | `design-intervention-evaluation` | C1, C3, C11, C13, C19, C23; C20–C22 si se evalúa intervención | Diseño causal, supuestos y gate de interpretación. |
| H05 | `evaluate-operational-selection` | C1, C4, C5, C14, C19–C21; C17 condicional; C23/C24 requieren H23/H24 | Política de selección y etiquetas; distinguir score, acción e impacto. |
| H06 | `forecast-backtesting` | C2, C12 | Evaluación por horizonte y decisión en dos familias de forecast. |
| H07 | `evaluate-grounded-assistant` | C6 | Respuestas con fuentes, permisos y abstención. |
| H08 | `synthesize-evidence-to-recommendation` | C1–C24 | Playbook/template existentes; evaluar necesidad adicional. |
| H09 | `reconcile-business-metrics` | C8, C15; C2/C12 si hay inconsistencias de medición | Definiciones, linaje y puente de reconciliación. |
| H10 | `design-entity-resolution` | C9 | Modelo de entidades, reglas y evaluación de matches. |
| H11 | `assess-decision-data-readiness` | C1–C5, C8–C15, C17–C24 | Revisar solapamiento con `understand-dataset` antes de crear otra skill. |
| H12 | `evaluate-document-extraction` | C10 | Schema, anotación y evaluación por campo/documento. |
| H13 | `evaluate-recommendation-policy` | C11 | Exposición, cold start y evaluación offline/online. |
| H14 | `audit-inherited-solution` | C14 | Contrato de auditoría y límites de reproducibilidad. |
| H15 | `diagnose-event-log-process` | C15 | Contrato de eventos, variantes y duración/completitud. |
| H16 | `define-agent-action-boundaries` | C16 | Contratos de herramientas y autoridad; no crea un agent automáticamente. |
| H17 | `design-operational-monitoring` | C5, C6, C9–C12, C14, C16–C24 si hay operación | Playbook de señales, umbrales, owners y respuesta. |
| H18 | `design-human-review-policy` | C4–C6, C9, C10, C14, C16; C17/C19/C21–C24 si hay revisión humana | Contrato/gates de revisión, abstención, capacidad y escalamiento. |
| H19 | `evaluate-probability-calibration` | C1, C4, C5, C17, C18, C20, C21, cuando se interpreta probabilidad | Evaluar probabilidad y discriminación por separado; scope temporal/población explícito. |
| H20 | `validate-delayed-outcome-targets` | C1, C4, C5, C17–C23 cuando el outcome está pendiente | Contrato/gate de outcome, horizonte, maduración y censura; revisar extensión de skills existentes. |
| H21 | `design-time-to-event-evaluation` | C5, C20–C22 si se elige tiempo hasta evento observable | Evaluación con evento, tiempos, censura y entrada de observaciones definidos. |
| H22 | `estimate-customer-lifetime-value` | C22 | Contrato de contribución/horizonte y procedimiento de estimación; separar inversión incremental. |
| H23 | `evaluate-uplift-targeting` | C23; C22 si se evalúa retención incremental | Extensión especializada de H04/H05 o skill; evidencia causal y evaluación de valor de política. |
| H24 | `design-unlabeled-anomaly-review` | C24 | Playbook de evaluación sin labels, muestreo y feedback; revisar scope frente a H11/H17/H18. |

Los escenarios nuevos también amplían H02–H05, H09–H11 y H17–H21 cuando aplican sus triggers. La cobertura ampliada y condiciones están registradas en las entradas correspondientes del registro.

Los inputs, outputs, checks, límites y ejemplos de evaluación se conservan en el [registro de hipótesis](2026-10-04-acos-candidate-hypotheses.md).

La cobertura alta de un patrón transversal no basta por sí sola para crear una skill: primero se compara la ejecución con el playbook/template existente y se identifica un fallo observable que una instrucción especializada pueda corregir.

## Estado de la exploración y posibles evaluaciones

1. **Evaluar lo existente con casos de distintos dominios.** Usar C1, C4 y C5 para contrastar `understand-dataset`, `detect-leakage`, `design-validation` y, cuando aplique, `build-features`. Usar C7 para `research-intelligence`. Capturar baseline, treatment, expected y límites sin tomar el resultado sintético como validación completa.
2. **Seguir contrastando hipótesis antes de elegir una primera tanda.** H01/H02/H03 conservan interés, pero los nuevos escenarios amplían la cobertura de causalidad, forecast, monitoreo y revisión humana. El registro muestra tanto procedimientos como posibles templates/gates.
3. **Resolver solapamientos y reunir evidencia de problema.** H11 puede extender una skill existente; H17/H18 pueden bastar como playbooks/contratos. Las fichas candidate ya tienen decisiones. Aplicar sus condiciones de reapertura/diferimiento; si surge un nuevo problema que justifique experimentar, completar evidencia y revisar el candidate gate del Foundry. Los casos sintéticos pueden aportar verificabilidad, sin fabricar antecedentes de uso real.

## Ejemplos de evaluación que podrían prepararse

- **Framing:** briefs deliberadamente ambiguos de C1, C4 y C7. Expected: decisión, owner, unidad, horizonte, KPI, restricciones y preguntas abiertas, sin inventar datos.
- **Impacto:** C1, C3 y C5 con costes/beneficios incompletos. Expected: baseline, supuestos, sensibilidad y separación entre impacto observado, simulado y esperado.
- **Restricciones:** C2, C4 y C5. Expected: función objetivo, restricciones, factibilidad, escenarios y explicación de lo que no puede optimizarse con los datos disponibles.
- **Skills actuales de Data Science:** C1, C4 y C5 con variaciones de temporalidad, panel, label delay y variables posteriores a la decisión. Expected: riesgos pertinentes y ausencia de reglas automáticas simplistas.

- **CLV:** C22 con márgenes ausentes, doble descuento del CAC y cohortes inmaduras. Expected: contrato de valor, límites de horizonte y presupuesto condicionado; no confundir valor residual con efecto de retener.
- **Uplift:** C23 con variables posteriores a la oferta, segmentos sin control y política elegida sobre su propio conjunto de evaluación. Expected: impedir inferencias causales sin soporte y preservar evaluación independiente bajo costes/capacidad.
- **Anomalías:** C24 con cambio operativo legítimo, referencia contaminada y feedback solo del top de alertas. Expected: distinguir rareza/utilidad, diseñar revisión/muestreo y no fabricar métricas supervisadas.

Estos ejemplos son material preparatorio. Un `case.md` y su `expected.md` se crearían en el Foundry solo después de revisar el candidate gate y aceptar el paso a experimento, preservando la separación de evaluación definida allí.

## Huecos de cobertura pendientes

Estos problemas todavía no tienen un escenario E2E propio en esta matriz; no se cuentan entre C1–C24.

- **Pérdidas crediticias y escenarios de estrés:** estimación y sensibilidad de componentes de pérdida y exposición. Originación/monitoreo no cubren esta tarea completa.
- **Churn involuntario:** fallos de pago, incidencias de facturación y recuperación de suscripciones, con acciones distintas de retención voluntaria.
- **Ubicación y diseño de redes:** elegir instalaciones, zonas o puntos de servicio; ruteo opcional en C4 no cubre diseño geoespacial completo.
- **Migración y confiabilidad de plataformas de datos:** backfills, schema evolution, pipelines, SLAs y aceptación de una migración; C9 cubre identidad/integración parcial.
- **ML serving en producción:** latencia, batch/online, training-serving skew, rollbacks y cambios de versión; monitoreo existente no equivale a un caso de ingeniería de serving.
- **AI de voz, imágenes o multimodal:** calidad de inputs, evaluación y experiencia distintas del asistente textual y extracción documental.
- **Planificación de inventarios multiescalón:** demanda, lead times y restricciones entre varios niveles de una cadena; C2 es una composición más simple.

Además, faltan variantes de estrés transversales: ausencia total de datos, desacuerdo de stakeholders sobre el KPI, cambios de scope, permisos/integraciones indisponibles y exigencias de explicabilidad o revisión por segmento. Estas se incorporarán a escenarios concretos antes de inferir nuevas skills. Las obligaciones del mercado o cliente se verifican en cada engagement.
