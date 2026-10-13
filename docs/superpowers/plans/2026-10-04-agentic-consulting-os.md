# Agentic Consulting OS modular — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convertir `AGENTIC_CONSULTING_OS.md` en un punto de entrada claro para un playbook modular de consultoría, con plantillas de proyecto y ejemplos sintéticos alineados al diseño aprobado.

**Architecture:** Mantener el manual raíz como resumen y mapa del OS. Mover las reglas operativas detalladas a documentos acotados en `workflow/`, `playbooks/` y `operations/`; separar las plantillas de proyectos y los ejemplos sintéticos. David Skill Foundry seguirá siendo la fuente canónica de plantillas, evaluaciones y promoción de capacidades.

**Tech Stack:** Archivos Markdown y enlaces relativos; sin dependencias de software ni integraciones externas.

**Spec:** `docs/superpowers/specs/2026-10-04-agentic-consulting-os-design.md`

## Global Constraints

- Redactar la documentación y las instrucciones operativas principalmente en español; conservar nombres oficiales y términos técnicos en inglés cuando sean más precisos.
- Mantener el Foundry como fuente de verdad para skills, agents, cases, expected results, evaluations y promoción de capacidades.
- Tratar los artifacts de proyecto/cliente y el ciclo de madurez de capacidades como flujos separados.
- No copiar datos o resultados de clientes al Foundry sin autorización; usar referencias sanitizadas o ejemplos sintéticos cuando corresponda.
- No presentar documentos Markdown como skills nativas instaladas ni asumir que una capacidad está disponible en un runtime sin comprobarlo.
- Mantener las herramientas como opcionales; el flujo mínimo no debe depender de Linear, Orca, MCP, OpenSpec, MLflow ni de un harness específico.
- Crear artifacts de proyecto solo cuando el trabajo los necesite; no exigir archivos vacíos.
- No inicializar Git ni configurar cuentas, proveedores, remotos, trackers o permisos externos como parte de este cambio documental.

## Review Focus

- **Foundry frente al ciclo del proyecto:** confirmar que los estados de capacidad nunca se utilicen como estados de proyectos o tareas; revisar en la Tarea 2.
- **Contexto sensible del cliente:** confirmar que las plantillas y ejemplos no contengan datos reales ni resultados no respaldados; revisar en la Tarea 7.
- **Disponibilidad en runtimes:** confirmar que el manual no equipare `stable` con estar instalado/visible en un harness; revisar en la Tarea 6.
- **Selección del método:** confirmar gates separados para análisis, causalidad, modelado, build y delivery, sin hacer ML por defecto; revisar en la Tarea 4.
- **Alcance de UI y límites de skills:** confirmar que la ruta UI sea condicional, que las tres skills tengan responsabilidades/precondiciones distintas y que visual QA no se confunda con usabilidad; revisar en la Tarea 5.
- **Deriva de fuentes de verdad:** confirmar que el manual raíz no duplique módulos ni plantillas del Foundry; revisar en la Tarea 8.

---

## Estructura de archivos

| Archivo | Responsabilidad |
|---|---|
| `AGENTIC_CONSULTING_OS.md` | Propósito, principios, inicio rápido, flujo resumido, navegación y límites prácticos. |
| `workflow/project-lifecycle.md` | Etapas de consultoría, gates, salidas y retornos. |
| `workflow/execution-and-qa.md` | Roles humano/agente, autoridad, contrato de tarea, niveles de revisión y cierre. |
| `workflow/isolation-and-context.md` | Límites entre clientes, acceso, contexto persistente y fuentes canónicas. |
| `workflow/capability-lifecycle.md` | Derivación al Foundry, candidate gate, uso por estado y distinción de runtime/versión. |
| `playbooks/data-understanding-analysis.md` | Comprensión de datos, calidad, SQL, EDA y análisis descriptivo/diagnóstico. |
| `playbooks/experiments-and-models.md` | Evaluación causal, diseño experimental, validación ML, leakage, diagnósticos y límites de impacto. |
| `playbooks/research-impact-delivery.md` | Evidencia de research, impacto de negocio, síntesis, storytelling ejecutivo y QA de delivery. |
| `playbooks/product-ui-and-prototyping.md` | Ruta condicional UX/UI, prototipos, handoff Figma y límites de validación. |
| `operations/tools-and-adoption.md` | Adaptadores de herramientas, bootstrap, adopción gradual y señales de éxito. |
| `templates/project-and-task.md` | Plantillas copiables de brief de proyecto y contrato de tarea. |
| `templates/data-and-validation.md` | Plantillas de contrato de datos y validación. |
| `templates/findings-and-qa.md` | Formatos de findings y revisión/QA. |
| `templates/delivery-and-handoff.md` | Manifest de delivery, handoff y cierre de sesión. |
| `examples/synthetic/card-activation.md` | Ejemplo sintético de punta a punta sin datos de clientes. |
| `docs/superpowers/specs/2026-10-04-agentic-consulting-os-design.md` | Diseño aprobado que gobierna esta migración. |
| `docs/superpowers/plans/2026-10-04-agentic-consulting-os.md` | Este plan. |

## Tareas de ejecución

### Tarea 1: Redactar el módulo del ciclo de consultoría

**Archivos:**
- Crear: `workflow/project-lifecycle.md`

**Interfaces:**
- Consume: ciclo aprobado en el spec, en particular las siete etapas y sus salidas.
- Produce: descripción operativa canónica de intake, framing, comprensión de datos, selección del método, ejecución, revisión, delivery y retornos.

- [x] **Paso 1: Definir el resumen del ciclo** con el diagrama aprobado y la regla de que el trabajo puede volver a una etapa anterior.
- [x] **Paso 2: Describir cada etapa** con su pregunta de decisión, salida esperada y condición de salida; indicar cuándo una tarea puede cerrarse, acotarse o continuar sin modelo.
- [x] **Paso 3: Definir la transición al routing** de `playbooks/` y la aceptación que debe estar clara antes de ejecutar.
- [x] **Paso 4: Revisar el módulo contra el diseño** para cubrir etapas, retornos y consistencia con las rutas `ANALYSIS`, `EXPERIMENT`, `MODEL`, `BUILD`, `RESEARCH`, `PRODUCT_UI` y `DELIVERY`.

**Criterio de aceptación:** El lector puede reconocer la etapa actual, su salida, la decisión siguiente y el retorno posible sin leer todo el OS.

### Tarea 2: Documentar el ciclo de capacidades del Foundry

**Archivos:**
- Crear: `workflow/capability-lifecycle.md`

**Interfaces:**
- Consume: David Skill Foundry como fuente canónica externa; ciclo y política de uso aprobados.
- Produce: punto de derivación de observaciones de proyectos al Foundry y reglas de uso por estado.

- [x] **Paso 1: Separar el ciclo de consultoría del ciclo Foundry**; mostrar su conexión y aclarar que estados de proyecto/tarea/entrega no utilizan el ciclo de capacidades.
- [x] **Paso 2: Definir el disparador de candidate** como problema recurrente, reutilizable y verificable que pasa el candidate gate; diferenciar procedimientos puntuales de candidates.
- [x] **Paso 3: Mapear cada estado al uso en proyectos** según el spec; aclarar que `evaluated` no significa éxito por sí solo y que el Foundry controla las transiciones formales.
- [x] **Paso 4: Definir los límites del contexto del cliente** para observaciones, evaluation cases y evidencia sintética/sanitizada.
- [x] **Paso 5: Revisar que no haya duplicación**; enlazar las plantillas canónicas del Foundry sin reproducirlas en el playbook.

**Criterio de aceptación:** El módulo no crea un Foundry paralelo, no promueve capacidades ni presenta un candidate como confiable para uso normal.

### Tarea 3: Redactar los módulos de ejecución, aislamiento y contexto

**Archivos:**
- Crear: `workflow/execution-and-qa.md`
- Crear: `workflow/isolation-and-context.md`

**Interfaces:**
- Consume: ciclo de la Tarea 1 y política de capacidades de la Tarea 2.
- Produce: límites de tarea, roles/autoridad, niveles de QA, aislamiento entre clientes y reglas de contexto/fuentes canónicas.

- [x] **Paso 1: Definir responsabilidades y autoridad** del consultor, ejecutor, reviewer y especialista opcional; mantener un ejecutor/integrador como valor por defecto.
- [x] **Paso 2: Especificar el contrato de tarea** con ID, objetivo/decisión, inputs, alcance de escritura/herramientas, restricciones, aceptación, salida, evidencia y handoff.
- [x] **Paso 3: Definir revisión proporcional y cierre común** para los niveles ligero, estándar y reforzado; incluir condiciones de parada/renegociación.
- [x] **Paso 4: Describir aislamiento** con repositorios/espacios separados por proyecto, identidad/recursos autorizados y la aclaración de que las carpetas/worktrees no son barreras de seguridad.
- [x] **Paso 5: Definir contexto persistente mínimo y fuentes canónicas**; explicar cuándo se necesitan PROJECT/brief, ACCESS, STATE, task, contrato de datos, validación, decisiones y tracker.
- [x] **Paso 6: Revisar límites de roles y fuentes canónicas** para encontrar contradicciones o estados duplicados.

**Criterio de aceptación:** Los módulos dejan claro quién decide, quién ejecuta, qué puede escribir, cuándo detenerse, qué persistir y cómo mantener acotado el contexto del cliente.

### Tarea 4: Extraer los playbooks metodológicos Data & AI

**Archivos:**
- Crear: `playbooks/data-understanding-analysis.md`
- Crear: `playbooks/experiments-and-models.md`
- Crear: `playbooks/research-impact-delivery.md`

**Interfaces:**
- Consume: routing y gates de la Tarea 1; niveles de revisión de la Tarea 3.
- Produce: guía metodológica por necesidad de decisión, no como fases obligatorias para cada proyecto.

- [x] **Paso 1: Documentar comprensión de datos y análisis:** grain, keys, joins, definiciones, disponibilidad de datos, auditoría de calidad, cohortes maduras, denominadores, evidencia SQL/EDA y límites causales.
- [x] **Paso 2: Documentar experimentos y modelos:** estimand/diseño, baseline, disponibilidad de features al momento de decisión, split temporal/por entidad cuando aplique, checks de leakage, métricas operativas, diagnósticos, estabilidad y diferencia entre propensión e impacto causal.
- [x] **Paso 3: Documentar research, impacto y delivery:** calidad/contradicciones de fuentes, supuestos de acción/coste/beneficio, findings trazables, storyline según audiencia, reconciliación numérica y revisión de entrega.
- [x] **Paso 4: Para cada ruta, declarar condiciones de entrada, artifacts mínimos, riesgos principales, evidencia de salida y motivos para no añadir complejidad.**
- [x] **Paso 5: Revisar cada playbook contra la tabla de rutas** para que sus gates sean distintos y ninguno imponga modelado por defecto.

**Criterio de aceptación:** El consultor puede seleccionar la ruta y reconocer su evidencia y límites sin tratar los playbooks como una secuencia obligatoria.

### Tarea 5: Añadir el playbook condicional de producto/UI

**Archivos:**
- Crear: `playbooks/product-ui-and-prototyping.md`

**Interfaces:**
- Consume: disparador y ruta `PRODUCT_UI` del spec; fuentes de las skills del Foundry para responsabilidades y precondiciones.
- Produce: flujo UX/UI portable, en español, que solo se consulta cuando el proyecto requiere una interacción de usuario.

- [x] **Paso 1: Definir el gate de activación:** empezar solo si se requiere una interacción nueva/modificada; de lo contrario, usar análisis/modelo/reporte o canal existente.
- [x] **Paso 2: Definir planificación UX proporcional** usando `ui-planning` en cambios no triviales: usuario/tarea/decisión, user flows, Information Architecture, inventario/specs de pantallas, states, dependencias, reglas de negocio, wireframes, assumptions y preguntas abiertas.
- [x] **Paso 3: Definir el gate de prototipo/diseño:** usar wireframes de baja fidelidad para resolver estructura; usar Figma/high fidelity solo si la alineación visual, revisión con stakeholders/usuarios o handoff a implementación lo justifica; requerir aprobación humana antes de usarlo como referencia de implementación.
- [x] **Paso 4: Declarar precondiciones de `figma-handoff`:** referencia Figma identificable y aprobada para handoff definitivo, repositorio inspeccionable y Design System/tokens existentes. Describir alternativa ligera si faltan.
- [x] **Paso 5: Declarar precondiciones y límites de `visual-qa`:** UI implementada y ejecutable, navegador/entorno disponible y referencia/criterios declarados; separar visual QA de usabilidad, comportamiento/reglas de negocio, accesibilidad y validación de modelos. Cuando la usabilidad sea una pregunta material, proponer validación de tareas con usuarios representativos si es posible; si no se realiza, dejarlo explícito.
- [x] **Paso 6: Añadir consideraciones de interfaces Data/AI** cuando correspondan: frescura, datos incompletos, estados no-score/fallo, incertidumbre, revisión/override humano y no presentar propensión como impacto causal.
- [x] **Paso 7: Registrar el estado actual del Foundry** con precisión: `ui-planning`, `figma-handoff` y `visual-qa` son `experimental 0.1.0` en las fuentes consultadas; comprobar estado/versión y disponibilidad en runtime antes de usarlas; excluir `design-validation` de UX/UI porque corresponde a validación de modelos supervisados.
- [x] **Paso 8: Revisar idioma y alcance:** redactar prosa operacional en español, conservar términos/skills útiles en inglés y no exigir Claude Code, Figma, Orca, shadcn, React/Next.js ni conectores.

**Criterio de aceptación:** El consultor puede decidir si requiere UI, elegir el artifact de diseño proporcional y reconocer qué tipo de validación ofrece cada skill.

### Tarea 6: Documentar herramientas opcionales y adopción

**Archivos:**
- Crear: `operations/tools-and-adoption.md`

**Interfaces:**
- Consume: distinción de runtime/capacidades de las Tareas 2 y 5 y reglas de fuentes/acceso de la Tarea 3.
- Produce: guía mínima de bootstrap/adopción con integraciones opcionales separadas.

- [x] **Paso 1: Definir comprobaciones de runtime** para visibilidad/nombre/versión de capacidades y diferenciar madurez Foundry, instalación y adopción en proyecto.
- [x] **Paso 2: Explicar la diferencia entre Markdown y runbook**; no llamar skill nativa a un documento no instalado ni prometer comportamiento no disponible.
- [x] **Paso 3: Agrupar Linear, Orca, MCP, Superpowers, OpenSpec, MLflow, Figma, Figma MCP, shadcn, 21st.dev, herramientas Python/SQL y otros adaptadores como opcionales** sujetos a necesidad y permiso, no como requisitos V1.
- [x] **Paso 4: Definir adopción gradual:** ejemplo sintético, uso en proyecto autorizado, retrospectiva, captura de candidates y automatización solo tras observar valor en un flujo manual recurrente.
- [x] **Paso 5: Definir señales observables de éxito** y medir una línea base antes de fijar objetivos; evitar promesas de productividad sin datos.
- [x] **Paso 6: Revisar las instrucciones de bootstrap** para preservar contenido existente, crear solo lo necesario, evitar setup externo y declarar límites reales.

**Criterio de aceptación:** Un proyecto puede usar el OS con un harness disponible y revisión humana, sin integraciones opcionales.

### Tarea 7: Extraer plantillas de proyecto y elaborar los ejemplos sintéticos

**Archivos:**
- Crear: `templates/project-and-task.md`
- Crear: `templates/data-and-validation.md`
- Crear: `templates/findings-and-qa.md`
- Crear: `templates/delivery-and-handoff.md`
- Crear: `examples/synthetic/card-activation.md`

**Interfaces:**
- Consume: contrato de tarea, fuentes canónicas, QA y gates de método de las Tareas 1, 3, 4 y 5.
- Produce: artifacts copiables y ejemplos ficticios de punta a punta.

- [x] **Paso 1: Extraer solo plantillas de proyecto** del manual actual; mantener externas las plantillas Foundry de capacidades/evaluación.
- [x] **Paso 2: Aclarar la opcionalidad** de cada plantilla: cuándo se necesitan ACCESS, data contract, validation, findings, QA y delivery manifest.
- [x] **Paso 3: Crear el caso de activación de tarjetas** con nombres ficticios y datos sintéticos; mostrar framing, contrato, análisis, QA, decisión con/sin modelo, recomendación y captura de candidate solo como ramal condicional. Incluir ruta UI solo si el ejemplo plantea una interacción de usuario.
- [x] **Paso 4: Incluir un ejemplo de seis repositorios de proyecto separados:** Aurora (activación), Boreal (retención/priorización), Cumbre (incrementalidad de campaña), Delta (calidad de datos), Estrella (pronóstico) y Faro (research). Mostrar `PRODUCT_UI` solo en Boreal, donde el score necesita una cola de trabajo para el analista; entregar Estrella como reporte por defecto, sin inventar una interfaz. Aclarar que el padre común es organizativo, no una barrera de seguridad.
- [x] **Paso 5: Revisar plantillas y ejemplos** para descartar aprobaciones inventadas, resultados sin sustento, datos reales accidentales o archivos vacíos obligatorios.

**Criterio de aceptación:** Las plantillas se pueden copiar selectivamente y los ejemplos demuestran el flujo sin presentar resultados ficticios como hechos de clientes.

### Tarea 8: Refactorizar el manual raíz e integrar los módulos

**Archivos:**
- Modificar: `AGENTIC_CONSULTING_OS.md`
- Referencia: todos los archivos creados en las Tareas 1–7.

**Interfaces:**
- Consume: módulos, plantillas y ejemplos aprobados.
- Produce: punto de entrada conciso con navegación relativa correcta y sin reglas detalladas en competencia.

- [x] **Paso 1: Conservar en el manual raíz** propósito, audiencia, principios, inicio mínimo, diagrama del flujo, límites de seguridad/autoridad, disparador condicional `PRODUCT_UI` y mapa.
- [x] **Paso 2: Reubicar el contenido detallado** de las 32 secciones actuales; preservar orientación útil de SQL, EDA, ML, impacto, QA, aislamiento, herramientas y delivery en sus módulos.
- [x] **Paso 3: Quitar duplicación** del raíz y sustituirla por resúmenes breves y enlaces relativos.
- [x] **Paso 4: Actualizar el índice y el prompt de quick start** para usar la estructura modular, preparar un proyecto mínimo y no crear todo el árbol por defecto.
- [x] **Paso 5: Quitar afirmaciones que impliquen** integraciones ya configuradas, procedimientos como skills instaladas o aislamiento de cliente mediante carpetas solamente.
- [x] **Paso 6: Revisar navegación, terminología y coherencia**; resolver nombres contradictorios, reglas repetidas y enlaces pendientes antes de presentar el resultado.

**Criterio de aceptación:** El manual raíz conserva su función de entrada; cada tema detallado tiene un módulo canónico y los enlaces/nombres corresponden a los archivos finales.

## Restricciones del workspace

El workspace actual no es un repositorio Git. No inicializar Git ni afirmar que hubo un commit. Si el trabajo se traslada a un repositorio versionado, podrán hacerse commits bajo el flujo existente del usuario.

Este es un cambio documental. No instalar herramientas, configurar sistemas externos ni crear/reubicar proyectos reales de clientes durante la implementación del playbook.

## Registro de ejecución

- **Pre-flight de interfaces:** Tarea 1 produce el ciclo usado por las Tareas 4, 5, 7 y 8; Tarea 2 define el ciclo Foundry consumido por las Tareas 5, 6 y 8; Tarea 3 aporta autoridad/acceso/fuentes para las Tareas 4, 6 y 7; las Tareas 4–7 aportan módulos y artifacts al índice de la Tarea 8. El spec aprobado resuelve los límites; no hay conflictos entre interfaces.
- **Ruling:** no crear worktree ni ledger bajo `.superpowers/sdd`; el workspace no tiene repositorio Git y el plan prohíbe inicializarlo. Se hará seguimiento con las casillas del plan y este registro — costo si estuviera equivocado: no habrá aislamiento ni historial Git para revertir por commit.
- **Ruling:** no añadir ni ejecutar tests de software; el alcance es documentación y el usuario no pidió pruebas. Revisar contenido, consistencia y referencias como parte de la aceptación documental — costo si estuviera equivocado: algún defecto editorial o enlace roto podría persistir.
- **Tarea 1: completa.** `workflow/project-lifecycle.md` contiene las etapas, outputs, gates, routing, retornos e intensidad aprobados. Revisión manual de encabezados, rutas y alineación con el spec.
- **Tarea 2: completa.** `workflow/capability-lifecycle.md` distingue conocimiento, procedimientos, candidates, skills y agents; conserva el Foundry como fuente canónica y documenta privacidad, estados y disponibilidad. Revisión manual contra `david-skill-foundry/AGENTS.md` y sus templates.
- **Tarea 3: completa.** `workflow/execution-and-qa.md` y `workflow/isolation-and-context.md` describen roles, límites de autoridad, contrato, QA, persistencia y fuentes canónicas. Revisión manual de responsabilidades y referencias a módulos.
- **Tarea 4: completa.** Los playbooks de datos/análisis, experimentos/modelos y research/impacto/delivery tienen gates propios y se enlazan con el ciclo. Revisión manual de encabezados, rutas y distinción de propensión/causalidad.
- **Tarea 5: completa.** `playbooks/product-ui-and-prototyping.md` define activación condicional, profundidad UX proporcional, gates humanos de diseño, precondiciones y límites de las tres skills, y riesgos de UI Data/AI. Revisión manual de idioma, estados del Foundry y enlaces relativos.
- **Tarea 6: completa.** `operations/tools-and-adoption.md` separa runbook de skill nativa, hace opcionales los adaptadores, ofrece bootstrap adaptable y define adopción/métricas sin prometer productividad. Revisión manual de permisos, fallbacks y referencias.
- **Tarea 7: completa.** Se añadieron cuatro plantillas de proyecto selectivas y un caso de activación explícitamente sintético, con un árbol de seis repositorios independientes y `PRODUCT_UI` condicional solo en Boreal. Revisión manual de opcionalidad, cifras marcadas como ilustrativas, privacidad y rutas enlazadas.
- **Tarea 8: completa.** `AGENTIC_CONSULTING_OS.md` ahora es mapa e inicio rápido del OS modular; la guía detallada se distribuye por workflow, playbooks, operaciones, templates y ejemplo. Revisión manual contra el spec y comprobación de enlaces Markdown locales: 0 rotos.
- **Revisión final:** reviewer independiente no encontró problemas críticos ni enlaces rotos; se actualizó el estado del spec para reflejar la aprobación del usuario y se tradujeron términos comunes al español donde no eran nombres oficiales o conceptos técnicos establecidos. Revisión manual posterior confirma coherencia con el plan.
