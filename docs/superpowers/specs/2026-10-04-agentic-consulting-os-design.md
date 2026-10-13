# Diseño: Agentic Consulting OS modular

**Estado:** aprobado por el usuario; implementado  
**Fecha:** 4 de octubre de 2026  
**Documento que se refinará:** `AGENTIC_CONSULTING_OS.md`  
**Audiencia:** consultor Data & AI / Data Science y agentes que colaboren en proyectos autorizados

## 1. Propósito

Refinar el manual actual para que sirva como sistema operativo práctico y portable para consultoría Data & AI / DS. Debe ayudar a convertir una pregunta de negocio en una recomendación revisable, con evidencia y límites claros, y facilitar retomar el trabajo sin depender del historial del chat.

El manual se dividirá en módulos operativos que puedan consultarse según la tarea. `AGENTIC_CONSULTING_OS.md` seguirá siendo el punto de entrada y expondrá el mapa y el flujo general.

## 2. Principios aprobados

1. **La decisión de negocio conduce el trabajo.** Datos, modelos y herramientas se eligen según la decisión que podrían cambiar.
2. **El consultor conserva el criterio y la responsabilidad.** Los agentes preparan análisis, alternativas y evidencia dentro de límites explícitos.
3. **La evidencia precede a la confianza.** Se separan hechos, inferencias, hipótesis y recomendaciones; se prefieren verificaciones deterministas cuando existen.
4. **El trabajo de cliente se aísla.** Un directorio no constituye por sí solo una barrera de seguridad; acceso, identidad, herramientas y permisos deben tener alcance autorizado.
5. **El Foundry gobierna las capacidades reutilizables.** El OS lo referencia y define cuándo derivar una oportunidad; no duplica sus plantillas ni decide promociones.
6. **El proceso se escala al riesgo.** La documentación, revisión, herramientas y cantidad de agentes deben ser proporcionales a la tarea.
7. **Primero comprender, luego estandarizar y automatizar.** No se añade infraestructura por anticipación.

## 3. Límites entre ciclos

El OS contiene dos ciclos conectados, pero distintos:

### Ciclo de consultoría

```text
Intake y límites
  → Enmarcar decisión
  → Entender y validar datos
  → Elegir método y alcance
  → Ejecutar con evidencia
  → Revisar y medir
  → Recomendar, entregar y cerrar
       ↺ volver a la etapa necesaria si fallan supuestos o gates
```

No es una cascada obligatoria. Un análisis puede terminar sin modelo; una brecha de datos puede detener, limitar o reorientar el alcance.

### Ciclo de capacidades del Foundry

El ciclo `problema/fuente → candidate → experimental → evaluated → validated → stable` aplica a skills, agents y otros artefactos reutilizables aceptados por el Foundry. No aplica al estado de proyectos, tareas ni entregables.

Cuando una tarea revela una necesidad que puede reaparecer, se registra una observación. Solo se crea un candidate si satisface el candidate gate del Foundry. A partir de ahí, el Foundry es responsable de templates, cases, baseline/treatment, evaluación, revisión y promoción humana. Un éxito puntual no implica crear una capacidad.

Los datos y resultados específicos del cliente no se copian al Foundry salvo autorización. Si esa autorización falta, la observación se sanitiza o se representa con datos sintéticos; se mantienen referencias no sensibles a la procedencia cuando sea permitido.

### Política operativa de uso por estado

| Estado Foundry | Uso propuesto desde un proyecto |
|---|---|
| `candidate` | Hipótesis pendiente; no se trata como capacidad confiable. |
| `experimental` | Pruebas de alcance controlado, supervisadas y revisadas. |
| `evaluated` | Consultar el resultado y la decisión de evaluación; el estado por sí mismo no significa éxito. |
| `validated` | Adopción supervisada en contextos respaldados por evidencia. |
| `stable` | Uso normal de la versión evaluada; cambios requieren la reevaluación indicada por el Foundry. |
| `rejected` / `deprecated` | No seleccionar para trabajo nuevo; conservar y respetar el registro/decisión. |

Esta es una política de uso del OS. El Foundry conserva autoridad sobre el significado formal de sus estados y las promociones.

### Ruta condicional de producto/UI

La interfaz es una ruta opcional, no una fase por defecto de los proyectos Data & AI. Se activa cuando la solución propuesta requiere una tarea o interacción de usuario que no puede resolverse adecuadamente con un canal o herramienta existente. Si el resultado se entrega como análisis, modelo, SQL, memo o presentación sin interacción nueva, no se abre esta ruta.

```text
confirmar usuario, tarea y decisión
  → estructurar experiencia si el cambio es significativo
  → validar flow/estructura con el stakeholder
  → acordar diseño visual si hace falta
  → handoff a implementación cuando esté en alcance
  → validar función, uso y visual por separado
```

- Para una pantalla o flujo no trivial, `ui-planning` puede producir user flows, Information Architecture, screen inventory, screen specifications, states, data dependencies, business rules y wireframes estructurales. La profundidad sigue el tamaño y riesgo del cambio.
- Los wireframes de baja fidelidad se usan para discutir estructura antes de estética. Figma/high fidelity se justifica si hay que alinear decisiones visuales, revisar una experiencia con stakeholders/usuarios o entregar una referencia clara a implementación. No es requisito si bastan criterios funcionales o la interfaz existente.
- El gate de diseño es humano. Una exploración, wireframe o frame no aprobado no es referencia oficial para implementación.
- `figma-handoff` aplica con referencia Figma identificable, repositorio inspeccionable y Design System/tokens existentes; para un handoff definitivo, la referencia debe estar aprobada. Si el proyecto no tiene Design System o repositorio, usar un handoff liviano sin fingir equivalencias de tokens o componentes.
- `visual-qa` aplica a UI implementada que pueda ejecutarse/inspeccionarse y con referencia o criterios declarados. Si faltan navegador, entorno o referencia, se declara la limitación; no se emite un PASS visual inventado.
- Visual QA no demuestra usabilidad, corrección de reglas de negocio, accesibilidad ni validez del modelo. Esas revisiones se especifican por separado según el riesgo. Cuando la usabilidad sea una pregunta importante, validar tareas con usuarios representativos si es posible; si no, registrar que no se validó.
- En interfaces de datos/AI, considerar frescura, datos incompletos, incertidumbre/no score, fallo del modelo y revisión/override humano cuando sean relevantes. No representar un score de propensión como impacto causal ni ocultar quién decide.

Las skills `ui-planning`, `figma-handoff` y `visual-qa` consultadas en el Foundry son `experimental`, versión `0.1.0`. Se pueden probar de forma controlada, bajo supervisión y con revisión del resultado. El OS no las presenta como skills estables ni garantiza que estén instaladas/visibles en un harness. `design-validation` no forma parte de esta ruta: diseña validaciones para modelos supervisados.

## 4. Flujo central y sus salidas

| Etapa | Pregunta o trabajo | Salida posible / condición de salida |
|---|---|---|
| Intake y límites | ¿Quién necesita decidir, cuándo, con qué contexto y bajo qué permisos? | Owner, deadline, alcance inicial y entorno/herramientas permitidos; si falta autorización, limitar a planificación o datos sintéticos. |
| Enmarcar decisión | ¿Qué acción podría cambiar? ¿Para quién, cuándo y con qué KPI? | Brief con población, horizonte, criterio de éxito y alcance acordado. |
| Entender y validar datos | ¿Qué representan las fuentes y permiten responder? | Contrato/auditoría cuando aplique; grain, definiciones, disponibilidad temporal, calidad y brechas visibles. |
| Elegir método y alcance | ¿Qué método responde la pregunta con riesgo y coste proporcionados? | Ruta, tarea y aceptación. Un modelo no es predeterminado. |
| Ejecutar con evidencia | ¿Qué resultado se obtiene de forma trazable y reproducible? | Código/consulta/run/findings aplicables, con fuentes, supuestos y verificaciones. |
| Revisar y medir | ¿Resiste checks metodológicos, numéricos y de robustez? | QA, impacto y límites; corregir, acotar o volver a una etapa previa si la evidencia no alcanza. |
| Recomendar, entregar y cerrar | ¿Qué debería hacer el owner y qué evidencia sostiene la recomendación? | Entrega revisada, aceptación o siguiente paso, estado actualizado y referencias a evidencia. |

`Roadmap` puede ser una salida proporcional a dependencias y alcance; no es un paso obligatorio antes de ejecutar toda tarea.

## 5. Arquitectura documental objetivo

```text
AGENTIC_CONSULTING_OS.md          # propósito, principios, quick start y mapa
workflow/
  project-lifecycle.md            # etapas, gates, salidas y retornos
  execution-and-qa.md             # roles, autoridad, contratos y revisión
  isolation-and-context.md        # límites entre clientes, memoria y acceso
  capability-lifecycle.md         # integración operativa con el Foundry
playbooks/
  data-understanding-analysis.md  # contratos, calidad, SQL y EDA
  experiments-and-models.md       # causalidad, validación y ML
  research-impact-delivery.md     # research, impacto y comunicación
  product-ui-and-prototyping.md   # ruta UI condicional, UX, prototipos y handoff
operations/
  tools-and-adoption.md           # herramientas opcionales, bootstrap y evolución
templates/
  project-and-task.md
  data-and-validation.md
  findings-and-qa.md
  delivery-and-handoff.md
examples/
  synthetic/card-activation.md
```

El mapa organiza documentos por unidad de uso, con pocos módulos. Los enlaces serán relativos y el documento raíz no duplicará explicaciones detalladas. Las plantillas de proyecto podrán derivarse del manual actual. No se copiarán al OS las plantillas `candidate.md`, `SKILL.md`, `agent.md`, `case.md`, `expected.md` ni `evaluation.md` del Foundry.

## 6. Routing metodológico

La selección de ruta parte de la decisión que se busca cambiar:

| Necesidad | Ruta | Gate principal |
|---|---|---|
| Entender contexto o alternativas | `RESEARCH` | Fuentes pertinentes, calidad de evidencia y contradicciones visibles. |
| Describir o diagnosticar qué ocurre | `ANALYSIS` | Grain, población, definiciones, denominadores y límites causales claros. |
| Estimar el efecto de una intervención | `EXPERIMENT` / evaluación causal | Estimand, diseño, supuestos y límites explícitos. |
| Priorizar casos para una acción | `MODEL` | La predicción habilita una acción operable; baseline, disponibilidad temporal, split y métricas son apropiados. |
| Mantener una lógica o sistema | `BUILD` | Contrato, criterios de aceptación, verificaciones y observabilidad adecuados. |
| Cambiar una tarea/interacción de usuario | `PRODUCT_UI` (condicional; puede combinarse con `BUILD`) | Existe una tarea de usuario que requiere una interfaz nueva/modificada; validar flow y datos antes de decidir wireframe, Figma o implementación. |
| Comunicar una decisión | `DELIVERY` | Hallazgos trazables, cifras reconciliadas y límites comprensibles para la audiencia. |

Principios metodológicos transversales:

- Una predicción de propensión no equivale a impacto causal o uplift.
- Para modelar se define la acción operativa, el target, la unidad, el horizonte y el cutoff antes de evaluar features.
- Las features deben estar disponibles al momento de decisión; el split y las transformaciones deben evitar leakage.
- Para análisis descriptivo y diagnóstico se aclaran grain, cohortes, denominadores y maduración de ventanas.
- Los experimentos definen estimand, asignación/unidad, guardrails, potencia cuando aplique y análisis antes de interpretar resultados.
- Si la evidencia no justifica complejidad adicional, se cierra sin esa complejidad.
- Para `PRODUCT_UI`, no iniciar por Figma o frontend: primero confirmar usuario, tarea, decisión, reglas y dependencias. Escalar de screen spec a wireframe, high fidelity y build según la incertidumbre y lo contratado.
- Separar validación de uso con personas, validación funcional/reglas, handoff semántico de Design System y visual QA; ninguna sustituye automáticamente a las demás.

## 7. Roles, autoridad y delegación

| Rol | Responsabilidad |
|---|---|
| Consultor | Problema, alcance, alineamiento, acceso autorizado, interpretación y aprobación/entrega final. |
| Agente ejecutor | Tarea acotada; usa solo inputs/herramientas permitidos, registra evidencia e incertidumbre. |
| Revisor | Busca errores metodológicos y de evidencia, con contexto independiente cuando el riesgo lo amerite. |
| Agente especialista | Ejecuta una unidad separable con interfaz y alcance de escritura definidos. |

Un agente ejecutor es el patrón por defecto. Se delega si la tarea es separable, sus entradas/salidas son claras y hay un integrador. Autoría, ejecución y revisión deben separarse cuando sea práctico para evaluaciones de capacidades; la regla exacta de Foundry prevalece allí.

Capacidad no equivale a autoridad. Agentes no amplían acceso, no cambian unilateralmente alcance/KPI, no promueven capacidades, no envían entregables ni modifican sistemas externos/producción sin autorización explícita. Las herramientas y operaciones permitidas se declaran por proyecto/tarea.

## 8. Contrato de tarea y fuentes canónicas

Cada tarea delegada explicita, en forma proporcional:

- identificador, proyecto y tipo;
- decisión/objetivo y aceptación;
- inputs y datos autorizados;
- alcance de escritura y herramientas;
- restricciones y presupuesto si corresponde;
- salida esperada, evidencia, límites y handoff.

Regla de una fuente canónica por dato operativo:

| Información | Fuente canónica propuesta |
|---|---|
| Prioridad/estado de tarea | Tracker aprobado; si no existe, índice local mínimo. Evitar dos estados editados manualmente. |
| Problema, decisión y alcance | Brief/`PROJECT`. |
| Definiciones de datos y validación | Contratos de datos/`VALIDATION` cuando la tarea lo requiera. |
| Decisiones, supuestos y estado de ejecución | Registro de decisiones/supuestos y `STATE`, solo cuando deba sobrevivir a la sesión. |
| Código, consultas y evidencia del proyecto | Repositorio/contexto autorizado del proyecto. |
| Skills, agents, cases y evaluaciones | David Skill Foundry. |
| Entregable publicado | Sistema de entrega autorizado. |

Un tracker referencia evidencia; no sustituye al repositorio como fuente de código/evidencia. La conversación no es la única memoria. No se exigen archivos vacíos: se crean cuando el trabajo necesita persistencia o revisión.

## 9. Calidad, gates y cierre

### Definición de cierre común

La tarea está completa cuando entrega lo acordado o documenta por qué no puede obtenerse; apunta a fuentes y verificaciones pertinentes; distingue hechos, inferencias, hipótesis y recomendaciones; deja límites y supuestos materiales visibles; y registra aceptación o un siguiente paso con owner.

### Niveles de revisión

| Intensidad | Aplicación | Revisión mínima |
|---|---|---|
| Ligera | Trabajo acotado y reversible | Autorrevisión y evidencia suficiente para comprobar/reproducir la conclusión. |
| Estándar | Múltiples fuentes o transformaciones mantenidas | Checks deterministas disponibles y revisión independiente de puntos críticos. |
| Reforzada | Decisión sensible, producción o compromiso externo | Validación ampliada, revisión independiente y aprobación humana antes de la acción pertinente. |

La intensidad añade verificación y juicio apropiados; no implica automáticamente más agentes o más documentos.

### Paradas y renegociación

Detener, limitar o renegociar cuando haya acceso no autorizado; KPI/población material sin definición; datos insuficientes; discrepancias críticas sin resolver; owner de decisión ausente; o acción irreversible fuera de la autorización. Se puede proponer planificación, fuente alternativa autorizada o datos sintéticos. No se cubren brechas críticas con supuestos silenciosos.

## 10. Runtime, herramientas y distribución de capacidades

La madurez de Foundry, instalación/visibilidad en el harness y adopción en un proyecto son dimensiones separadas. Antes de usar una capacidad se comprueba qué runtime la ofrece y qué versión. La distribución/copia conserva nombre, versión y referencia al origen canónico; no se edita como otra copia fuente. Un Markdown invocable no se describe como skill nativa instalada.

La V1 opera con repositorio autorizado, harness disponible y revisión humana. Linear, Orca, MCP, Superpowers, OpenSpec, MLflow, Figma, Figma MCP, shadcn, 21st.dev, proveedores y otros conectores son adaptadores opcionales; se incorporan ante necesidad y permiso. No se afirman capacidades que el entorno real no expone. Ninguna autorización en este manual aprueba por sí sola el uso de datos, cuentas o herramientas de un cliente.

## 11. Adopción y señales de éxito

1. Preparar módulos, plantillas de proyecto y un ejemplo sintético de punta a punta.
2. Aplicar lo necesario en un proyecto autorizado y registrar fricción, bloqueos y retrabajo.
3. Revisar hallazgos; derivar al Foundry solo patrones repetibles y verificables que pasen su candidate gate.
4. Automatizar un flujo manual entendido cuando su entrada/salida sean estables y exista señal de valor.

Señales: capacidad de retomar desde `STATE`; trazabilidad de cifras a evidencia; defectos relevantes detectados antes de compartir; retrabajo por alcance; y coste/tiempo en tareas comparables si los datos están disponibles. Se mide línea base antes de fijar objetivos cuantitativos. No se prometen mejoras porcentuales sin medición.

## 12. Migración desde el manual actual

- Conservar decisiones útiles sobre aislamiento, contratos, datos, metodología, storytelling y riesgos, actualizándolas contra este diseño.
- Reducir el documento raíz a propósito, principios, quick start, diagrama del flujo y mapa de navegación.
- Reubicar prácticas analíticas/modelado, roles/QA, seguridad/contexto y Foundry en los módulos indicados.
- Separar integraciones y herramientas opcionales del camino mínimo.
- Extraer del workflow frontend existente las pautas transferibles de UX, gates de diseño, Figma handoff y validación visual hacia `playbooks/product-ui-and-prototyping.md`; conservar Claude Code, Figma, Orca, shadcn, React/Next.js y conectores como adaptadores opcionales, no requisitos del OS.
- Referenciar `ui-planning`, `figma-handoff` y `visual-qa` por nombre y estado/versión observados, sujetos a comprobación de disponibilidad y evolución en el Foundry. No incorporar `design-validation` como skill UX/UI.
- Adaptar el bootstrap para leer instrucciones existentes, preservar datos del workspace, crear lo mínimo necesario, distinguir procedimientos Markdown de skills instaladas y no configurar sistemas externos.
- Extraer solo plantillas de proyecto útiles. No declarar aprobaciones corporativas, instalaciones, accesos, datos o evaluaciones inexistentes.
- Transformar el caso de activación de tarjetas en un ejemplo exclusivamente sintético, sin resultados presentados como hechos.
- Mantener español como idioma principal y términos/nombres oficiales cuando ayuden a la precisión.

## 13. Fuera de alcance

- Implementar el OS, instalar o promover skills/agents.
- Modificar el David Skill Foundry o duplicar su contenido canónico.
- Configurar cuentas, proveedores, MCP, Linear, Orca, MLflow, remotos Git o permisos corporativos.
- Proveer políticas oficiales de empleadores/clientes o suponer acceso a sus entornos.
- Construir una plataforma propia, un dashboard o automatización antes de demostrar necesidad.
- Publicar/entregar contenidos a terceros.

## 14. Supuestos y puntos de extensión

- El OS será personal, portable entre proyectos y adaptable a harnesses distintos.
- Se puede consultar el Foundry en el entorno del usuario, pero el manual no depende de una ruta absoluta local.
- El cliente/empleador define políticas, permisos, clasificación y herramientas aprobadas; el OS exige registrarlos, no los inventa.
- El OS contempla diseño de interfaces solo en proyectos que lo requieran; el estimado inicial de frecuencia es una hipótesis de planificación, no una métrica contractual.
- Las plantillas de proyecto se crean para apoyar el proceso; las plantillas de capacidades/evaluación permanecen en el Foundry.
- Si el archivo raíz y los módulos resultan difíciles de mantener, se podrá revisar la agrupación con evidencia de uso.

## 15. Criterio de aceptación del diseño

El usuario aprobó el diseño. La implementación conserva los criterios acordados:

- ambos ciclos y sus límites están representados correctamente;
- el mapa modular preserva el uso de `AGENTIC_CONSULTING_OS.md` como punto de entrada;
- Foundry conserva las plantillas y autoridad de promoción;
- métodos, roles, seguridad, QA y adopción reflejan las decisiones acordadas;
- la ruta de producto/UI se activa por necesidad, distingue las tres skills y mantiene en español la guía operacional, con términos e identificadores técnicos en inglés cuando corresponda;
- el texto separa propuesta operativa de política corporativa y capacidades realmente instaladas.
