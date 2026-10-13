# Diseño: ACOS Project Compiler

**Estado:** diseño base aprobado por el usuario  
**Fecha:** 4 de octubre de 2026  
**Producto:** CLI portable de Agentic Consulting OS  
**Audiencia:** consultor Data & AI / Data Science que inicia proyectos con Codex o Claude Code

## 1. Resumen

`acos` será un Consulting Project Compiler instalable. Recibirá contexto de negocio, tipo de engagement, datos, restricciones, entregables, etapa actual y runtime; propondrá una composición modular; y, tras confirmación humana, generará un workspace de consultoría con instrucciones, manual, estado, quality gates y snapshots seleccionados.

La entrada canónica del compiler será `project-profile.yaml`. El proceso no parte de una plantilla fija ni de un catálogo de skills asumido como confiable: clasifica el engagement con reglas locales, contrasta sus necesidades con Foundry, expone cobertura y brechas, y espera confirmación antes de escribir.

## 2. Objetivo y resultado esperado

Una persona instala ACOS una vez y puede ejecutar `acos init` desde cualquier ubicación en macOS, Linux o Windows. El proyecto generado le permite empezar con una guía específica de su caso y continuar con Codex, Claude Code o ambos.

El resultado exitoso debe:

- conectar el trabajo con una decisión de negocio y una medida de éxito;
- seleccionar solo etapas, capacidades y artefactos pertinentes;
- explicar por qué se eligió cada capacidad y cuándo usarla;
- respetar el ciclo y las plantillas canónicas del David Skill Foundry;
- hacer visibles la madurez y procedencia de skills experimentales;
- poder transportarse como workspace sin depender de la laptop que lo creó;
- dejar al consultor el control sobre clasificación, composición y avance de etapas.

## 3. Principios de diseño

1. **La necesidad determina el artefacto.** Una capacidad puede expresarse como pauta, template, gate, playbook o skill. No toda necesidad crea una skill.
2. **La decisión precede a la técnica.** No inferir ML, UI, GenAI o software por defecto.
3. **Composición modular.** Las etapas, carpetas, skills y controles se generan según el perfil confirmado.
4. **Reglas locales primero.** El classifier funciona sin LLM ni transmisión de contexto.
5. **La persona confirma.** La clasificación y el plan de compilación se revisan antes de escribir archivos.
6. **Foundry es fuente canónica.** ACOS consulta sus artefactos; no crea un lifecycle paralelo ni promueve estados.
7. **Los snapshots son explícitos y trazables.** Cada snapshot conserva fuente, madurez, versión e integridad.
8. **El feedback no altera autoridad.** El uso deja observaciones locales; los cambios de estado siguen siendo responsabilidad del Foundry.
9. **Portabilidad real.** Rutas relativas, formatos de texto comunes y sin enlaces simbólicos como requisito.

## 4. Arquitectura conceptual

```text
acos init
   │
   ├─ localizar o configurar Foundry local
   ├─ intake adaptativo
   ├─ classifier por reglas locales
   ├─ project-profile.yaml editable/confirmado
   ├─ resolver de capacidades
   ├─ inventario Foundry + análisis de cobertura
   ├─ vista previa de composición y archivos
   ├─ confirmación humana
   └─ compiler → workspace modular
```

El resolver separa tres conceptos:

1. **Arquetipos:** qué patrón de decisión busca resolver el engagement.
2. **Capacidades:** qué trabajo debe poder realizar el equipo/agente.
3. **Artefactos:** con qué pauta, skill, playbook, template o gate se habilita ese trabajo.

## 5. Mapa de capacidades

### 5.1 Ciclo de consultoría

Cada etapa tiene objetivo, resultados requeridos y un gate de salida. El punto de entrada se ajusta a la madurez real del proyecto; no es obligatorio recorrer todas las etapas desde cero.

1. **Discovery y contexto:** negocio, stakeholders, proceso, datos y restricciones.
2. **Framing:** decisión, owner, métrica de éxito, alcance y supuestos.
3. **Diagnóstico y evidencia:** estado actual, fuentes, hipótesis y brechas.
4. **Diseño y ejecución:** realizar el análisis o solución seleccionada.
5. **Validación:** solidez metodológica y utilidad para la decisión.
6. **Recomendación y delivery:** opciones, impacto, riesgos y entregables.
7. **Handoff y cierre:** responsables, límites, próximos pasos y monitoreo cuando aplique.

Los gates pueden dejar pendientes o devolver el trabajo a una etapa anterior. `acos validate` nunca mueve automáticamente el proyecto a la etapa siguiente.

### 5.2 Arquetipos de decisión

Se pueden combinar. Orientan la selección de capacidades, sin imponer una tecnología.

- `DIAGNOSE`: explicar qué ocurre y cuáles son sus causas probables.
- `PREDICT`: estimar un resultado para un caso o entidad.
- `FORECAST`: estimar volumen o valor a través del tiempo.
- `PRIORITIZE_SELECT`: ordenar o elegir casos bajo capacidad limitada.
- `OPTIMIZE`: encontrar una combinación de acciones bajo objetivos y restricciones.
- `EXPERIMENT_CAUSAL`: estimar el efecto de una intervención.
- `SEGMENT`: identificar grupos con necesidades o comportamientos distintos.
- `RECOMMEND`: sugerir una acción para un caso, usuario o contexto.

### 5.3 Formas de entrega

Son ortogonales a los arquetipos y pueden cruzarse con ellos:

- análisis o recomendación;
- automatización de proceso;
- producto de datos o AI;
- operación/producción de una solución.

### 5.4 Familias de capacidades

- **Consultoría y decisión:** descubrimiento, framing, hipótesis, métricas, evidencia, supuestos, riesgos, business case y recomendaciones.
- **Datos y métodos analíticos:** comprensión de fuentes/datasets, calidad, SQL, EDA, estadística, visualización e incertidumbre.
- **Métodos según arquetipo:** diagnóstico/causas; predicción/validación; forecasting/backtesting; ranking/priorización; optimización/escenarios; experimentación/causalidad; segmentación y recomendación.
- **Solución y adopción:** ingeniería de datos, AI/GenAI, software/UX, despliegue, monitoreo, seguridad, comunicación, handoff y adopción.

Controles transversales como privacidad, sesgo, reproducibilidad y trazabilidad activan revisiones según el perfil y el riesgo.

## 6. Intake y perfil del proyecto

### 6.1 Wizard adaptativo

El wizard tendrá como objetivo no exceder aproximadamente 12 preguntas obligatorias. Las preguntas condicionales aparecen solo cuando una respuesta las vuelve pertinentes.

Bloques:

1. Contexto: nombre del proyecto, industria, mercado y rol.
2. Decisión/problema: qué decisión se necesita y qué situación la motiva.
3. Éxito/personas: métrica de éxito, decisor y usuarios.
4. Trabajo probable: arquetipos propuestos y editables.
5. Datos/restricciones: fuentes y características relevantes; restricciones operativas.
6. Delivery/estado: entregables y etapa actual.
7. Runtime: Codex, Claude Code o ambos.

Se puede omitir o marcar confidencial la identidad del cliente.

### 6.2 Clasificación

- El classifier local se basa en reglas deterministas y señales explícitas del perfil.
- Cada propuesta muestra la señal que la motivó y una indicación de certeza.
- La persona puede aceptar, corregir, dejar sin resolver o añadir un arquetipo.
- El LLM es opcional y explícito. Antes de usarlo, ACOS muestra qué contexto se enviaría y solicita consentimiento. Sin consentimiento o servicio disponible, el flujo continúa localmente.
- No se envía contexto del cliente automáticamente.

### 6.3 Contrato canónico

Las respuestas confirmadas se escriben en `.acos/project-profile.yaml`. El perfil contiene como mínimo:

- identidad y contexto no sensible disponible;
- decisión, problema, éxito y stakeholders;
- arquetipos confirmados y estado de certeza;
- etapa inicial;
- fuentes/características de datos pertinentes;
- restricciones;
- entregables;
- runtimes objetivo.

El perfil, y no el texto conversacional ni el LLM, es la entrada reproducible al Module Resolver y Project Compiler.

## 7. Resolver de capacidades y cobertura de Foundry

### 7.1 Entradas y reglas

El resolver combina arquetipos, datos, restricciones, entregables, etapa y runtimes. Las reglas proponen capacidades; no deducen información de negocio no provista. La persona confirma o corrige el resultado.

### 7.2 Inspección del Foundry

Por cada capacidad requerida, el resolver inspecciona artefactos compatibles y evalúa:

- correspondencia de propósito y trigger;
- generalidad y límites del contexto original;
- evidencias y madurez;
- compatibilidad con runtime;
- duplicidad frente a otros artefactos;
- si el objeto correcto es skill, playbook, plantilla, gate, pauta o conocimiento.

La procedencia hackathon/específica se registra como contexto de evaluación; por sí sola no obliga a incluir ni excluir una skill. El contenido y la pertinencia para el proyecto determinan el match.

### 7.3 Política de madurez

| Estado en Foundry | Tratamiento en ACOS |
|---|---|
| `candidate` | Registrar como hipótesis/brecha; no incluir como skill operativa por defecto. |
| `experimental` | Fuente utilizable para un proyecto si hay match y confirmación humana. Mostrarla como provisional, fijar versión/hash y permitir feedback. |
| `evaluated` | Mostrar alcance y resultados; confirmar selección explícita. |
| `validated` | Elegible en los contextos respaldados; confirmar selección y conservar límites. |
| `stable` | Elegible cuando corresponda al engagement, sujeto a pertinencia y confirmación de composición. |
| `rejected` / `deprecated` | Excluir de proyectos nuevos salvo una decisión de revisión explícita documentada en Foundry. |

Usar una skill experimental no la promueve, valida ni modifica. Las transiciones formales las controla el Foundry.

### 7.4 Vista previa

Antes de generar archivos, ACOS presenta:

- capacidades seleccionadas y motivo;
- fuente, estado, versión, restricciones y runtimes de cada skill;
- cobertura parcial y límites;
- brechas sin artefacto compatible;
- capacidades excluidas y motivo;
- estructura de carpetas y artifacts que se crearían.

La persona confirma la composición final. ACOS no crea una skill automáticamente para llenar una brecha; puede proponer otro tipo de artefacto o dejar una oportunidad documentada.

### 7.5 Criterios de creación/evaluación futura

Antes de proponer un nuevo candidate, revisar si el problema reaparece fuera del contexto original; distinguir procedimiento reusable de detalles locales; comparar resultado con baseline; verificar outputs y límites; revisar solapamiento; y proteger datos del cliente en casos/evaluaciones.

## 8. Foundry local y transferencia entre dispositivos

- En el primer uso, ACOS intenta detectar Foundry local y, si no lo encuentra, solicita su ruta una vez por dispositivo.
- La ruta se guarda en configuración del usuario, fuera de proyectos de cliente.
- La carpeta Foundry disponible hoy no tiene repositorio Git/remoto configurado. ACOS V1 no dependerá de una conexión remota.
- Si Foundry no está accesible, `acos init` podrá continuar y dejar las capacidades correspondientes como brechas; no fabricará snapshots.
- Cada laptop requiere acceso a su propia copia local de Foundry. El mecanismo de sincronización de esas copias queda fuera de la V1.
- Una vez creado el proyecto, sus snapshots seleccionados son locales y portables; el proyecto no depende de la ruta Foundry del dispositivo inicial.

## 9. Feedback de uso de skills

Cada snapshot de skill mantiene el mismo status que Foundry en el momento de compilarse. El manifest registra procedencia, versión y hash.

El proyecto permite observaciones locales: útil, parcialmente útil o falló; tarea donde se usó; evidencia y límites observados. En revisión/cierre se puede resumir la observación para que una persona decida si propone un caso, ajuste o candidate en Foundry.

No hay promoción ni sincronización automática. Antes de trasladar una observación al Foundry, revisar y anonimizar; no copiar datos confidenciales del cliente sin autorización.

## 10. Workspace compilado

### 10.1 Núcleo común

```text
<proyecto>/
├── MANUAL.md
├── PROJECT.md
├── STATE.md
├── TASKS.md
├── DECISIONS.md
├── CAPABILITIES.md
├── AGENTS.md
├── .acos/
│   ├── project-profile.yaml
│   ├── manifest.yaml
│   ├── modules.yaml
│   └── state.yaml
└── ...módulos y artifacts seleccionados...
```

No se crean carpetas vacías solo por estar en un catálogo. Datos, análisis, modelado, validación, delivery, UI y otras áreas se crean según el perfil confirmado. `evidence/`, `playbooks/`, `templates/` y snapshots se incluyen según su selección.

### 10.2 Runtime e instrucciones

- `AGENTS.md` es la fuente compartida de instrucciones del proyecto.
- Las instrucciones generales no se duplican por runtime.
- Para Codex, las skills seleccionadas se copian a `.agents/skills/<name>/SKILL.md`.
- Para Claude Code, se copian a `.claude/skills/<name>/SKILL.md`.
- Si ambos están configurados, el mismo contenido/version/hash se copia a ambas rutas nativas y el manifest registra ambas.
- `CLAUDE.md` solo se crea como puente mínimo hacia `AGENTS.md` si la configuración necesaria para ese entorno lo requiere; no contiene otro OS.

### 10.3 Manual diario

`MANUAL.md` guía la próxima acción con etapa actual, objetivo, preguntas por responder, outputs requeridos, capacidades pertinentes, gate y siguiente etapa propuesta. `STATE.md` registra estado persistente; `TASKS.md` mantiene NOW/NEXT/LATER/BLOCKED de tamaño manejable; `CAPABILITIES.md` da razón, momento de uso, madurez y límites.

## 11. CLI V1

### `acos init [nombre] [--here]`

- Por defecto crea subcarpeta nueva dentro de la ubicación actual.
- `--here` inicializa la carpeta actual explícitamente.
- Ejecuta configuración local Foundry si es primer uso, intake, clasificación, resolución, vista previa y confirmación.
- Evita sobrescribir contenido existente sin una política explícita de conflicto. El caso `--here` debe detectar conflictos y presentarlos antes de escribir.

### `acos status`

Lee el manifest y estado locales; muestra proyecto, etapa, avance, bloqueos, preguntas y gate siguiente. No cambia el estado.

### `acos next`

Sugiere próximo objetivo, artifacts y preguntas; usa manual, etapa, tareas y capacidades compiladas. No adelanta estado ni ejecuta side effects externos.

### `acos validate`

Revisa presencia/estructura de artifacts y checks deterministas del gate indicado. Informa `PASS`, `NEEDS_REVIEW` o `BLOCKED` cuando corresponda, con la evidencia o requisito faltante. Los juicios cualitativos continúan requiriendo revisión humana. No mueve automáticamente la etapa.

Quedan fuera del alcance inicial `acos update`, sync remoto, marketplace, dashboard, gestión cloud y promoción automática de capacidades.

## 12. Instalación y plataforma

- Distribuir ACOS como paquete Python CLI.
- Instalación recomendada: `uv tool install agentic-consulting-os`; alternativa documentada: `pipx install agentic-consulting-os`.
- Una instalación global por usuario permite invocar `acos` desde cualquier ubicación.
- macOS, Linux y Windows son objetivos V1; cubrir diferencias de shell, rutas, permisos y finales de línea sin depender de symlinks.
- Claude Code y Codex son runtimes objetivo. El workspace sigue siendo Markdown/YAML portable incluso si no hay runtime disponible.
- Documentación de las herramientas: [uv tools](https://docs.astral.sh/uv/concepts/tools/) y [instalación pipx](https://pipx.pypa.io/latest/how-to/install-pipx.html).

## 13. Seguridad y privacidad

- El clasificador local no transmite datos.
- El uso de LLM es opt-in y muestra previamente qué contexto saldría del equipo.
- La ruta local de Foundry se guarda en configuración de usuario, no en el workspace de cliente.
- El proyecto contiene únicamente snapshots seleccionados. Ninguna autorización de compilación equivale a autorización para procesar datos externos ni conectar cuentas.
- Feedback queda en proyecto hasta revisión humana; no hay upload/sync de datos.
- Inicialización no debe borrar archivos ni modificar entornos globales aparte de su propia configuración declarada.

## 14. Criterios de aceptación del diseño

1. Un perfil confirmado permite reproducir la composición sin releer la conversación.
2. Las propuestas del classifier indican señales y son corregibles.
3. Se puede inicializar con solo reglas locales y sin conexión LLM.
4. El resolver muestra cobertura, límites, brechas y exclusiones antes de compilar.
5. Las skills experimentales pueden usarse bajo estado provisional y confirmación, sin promoción implícita.
6. El manifest permite identificar exactamente fuente, estado, versión, hash y rutas de cada snapshot.
7. Workspace de ambos runtimes conserva instrucciones comunes y skills nativas.
8. El proyecto generado sigue siendo utilizable si Foundry no está disponible después de inicializarlo.
9. `status`, `next` y `validate` no avanzan etapas automáticamente.
10. `--here` no sobrescribe contenido sin inspección y confirmación.
11. No se crean módulos ni carpetas que no correspondan a la composición confirmada.
12. Las observaciones no mutan el Foundry ni transfieren datos de cliente automáticamente.

## 15. Fuera de alcance

- Sincronizar Foundry entre dispositivos o acceder al Foundry mediante remoto.
- Actualización automática de snapshots, `acos update` y migraciones de perfiles.
- Marketplace de skills, catálogos públicos o promoción automática.
- LLM automático, envío silencioso de contexto o servicios cloud obligatorios.
- Generación/promoción automática de skills/agents/candidates.
- Dashboard visual o aplicación desktop.
- Crear todas las carpetas, todas las skills o todas las etapas en cada proyecto.
- Cambiar el contenido de `AGENTIC_CONSULTING_OS.md` como parte de este diseño. La relación e integración con ese manual se especificará al planificar implementación.

## 16. Decisiones aún abiertas para planificación

Estas decisiones pertenecen al plan técnico, no cambian el comportamiento de producto aprobado:

- estructura exacta y schema versionado de `project-profile.yaml`, manifest, modules y state;
- formato/versionado del catálogo y cómo detectar nombres de archivo de skills en Foundry;
- interfaz de almacenamiento de preferencias multiplataforma;
- política precisa de conflictos y reanudación durante `init`;
- distribución PyPI, versionado de paquetes y automatización de release;
- estructura concreta del catálogo inicial de módulos, templates y gates;
- definición de reglas deterministas y confianza explicable por regla.

## 17. Integración del spec existente

El spec [Agentic Consulting OS modular](2026-10-04-agentic-consulting-os-design.md) describe el método de consultoría. Este documento describe un compiler portable que instancia un proyecto usando ese método y snapshots del Foundry. La implementación debe mantener ambas responsabilidades separadas y definir su interfaz antes de modificar el manual o construir la CLI.

## 18. Auditoría inicial del inventario existente

Esta revisión registra los archivos presentes en `experiments/skills/` al 4 de octubre de 2026 y su ajuste inicial al dominio de ACOS. No es una evaluación formal del Foundry ni una decisión de promoción. Los nueve archivos de skill presentes indican estado `experimental`, versión `0.1.0`. El directorio `stable/` inspeccionado no contiene `SKILL.md`; en `cases/` y `evals/` no se encontró cobertura comparable de estas skills a través de varios engagements.

| Skill actual | Lectura inicial para el Module Resolver |
|---|---|
| `understand-dataset` | Capacidad técnica pertinente al recibir fuentes desconocidas. Condicional a trabajo de datos; no reemplaza discovery ni framing de negocio. Su candidate registra EQUANS como contexto de origen. |
| `detect-leakage` | Pertinente para trabajo supervisado con target, pipeline o validación. Requiere confirmar disponibilidad temporal y semántica del negocio. Su candidate registra EQUANS como contexto de origen. |
| `design-validation` | Pertinente para diseñar validación de modelos supervisados. Requiere contexto de producción, entidad, tiempo y decisión. Su candidate registra EQUANS como contexto de origen. |
| `build-features` | Solo aplica a ML supervisado y feature engineering. No es capacidad base de toda consultoría; revisar su alcance antes de incluirla. Su candidate registra EQUANS como contexto de origen. |
| `research-intelligence` | Opción para research técnico o de negocio que requiere comparar familias de solución y evidencia de fuentes disponibles. |
| `ui-planning` | Opción de producto/UI cuando existe una interacción de usuario que diseñar; no se activa por entregar un análisis o reporte. |
| `figma-handoff` | Opción de handoff cuando hay Figma, implementación y un Design System pertinente; el procedimiento describe Figma, React y shadcn/ui. |
| `visual-qa` | Opción para inspeccionar una UI implementada; su procedimiento depende de Orca Browser/Design Mode y de una referencia o criterios visuales. |
| `run-skill-eval` | Herramienta de workflow del Foundry para comparar baseline y treatment de una skill. No es parte normal de un proyecto de consultoría; se usaría para evaluar capacidades dentro del Foundry. |

El Module Resolver consultará los archivos de skills que existan realmente en la ruta Foundry configurada y verificará su metadata en cada inicialización. La procedencia de hackathon es contexto para valorar generalización; el match depende del propósito, trigger, límites, madurez y evidencia. La confirmación humana hace explícita la adopción provisional de una skill `experimental`.

## 19. Simulaciones de cobertura

El [análisis de veinticuatro engagements hipotéticos](../analysis/2026-10-04-acos-business-simulations.md) recorre el ciclo de consultoría completo, con ramas de fallo y cambio de alcance, para identificar cobertura del Foundry actual, brechas y posibles candidates. Incluye riesgo de crédito, varias formas de churn, CLV, uplift y anomalías sin labels, además de un backlog de problemas aún sin escenario E2E. El [registro acumulativo de hipótesis](../analysis/2026-10-04-acos-candidate-hypotheses.md) conserva triggers, inputs, outputs, checks, límites y solapamientos de veinticuatro capacidades potenciales. Es un ejercicio de diseño: sus frecuencias representan casos simulados y no evidencian recurrencia real ni justifican promoción de skills.


Las 24 hipótesis se documentaron como candidates en el Foundry usando su template canónico. El [mapa de candidates y solapamientos](../analysis/2026-10-04-acos-foundry-candidate-map.md) enlaza las fichas y propone extensiones/playbooks/contratos antes de crear skills independientes. La [revisión del 6 de octubre](../analysis/2026-10-06-acos-foundry-integration.md) actualiza las decisiones: 18 fichas se mantienen como conocimiento y seis están diferidas. Tres skills probadas se archivaron en scratch, conservando evidencia; las extensiones de validación vuelven a `0.1.0`. El inventario operativo permanece en nueve skills experimentales. Estas decisiones no bloquean el compiler ni autorizan reabrir candidates automáticamente.
