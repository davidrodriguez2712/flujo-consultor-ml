# Agentic Consulting OS (ACOS)

**Un método y una herramienta para llevar un proyecto de consultoría Data & AI de la pregunta de negocio a una recomendación defendible, trabajando con un agente de IA (Claude Code o Codex) y sin saltarte pasos.**

ACOS crea una carpeta de proyecto ordenada (un *workspace*) con el manual, las etapas, las plantillas y las skills que tu agente necesita. Después te dice en qué etapa estás, qué falta y si puedes avanzar.

> **Regla de oro:** el agente hace el trabajo; **tú decides y apruebas**. ACOS nunca avanza una etapa por su cuenta: para pasar necesita que el entregable esté completo **y** que tú registres tu aprobación.

### Míralo en 82 segundos

[![Video: el flujo de ACOS paso a paso](docs/video/preview.gif)](docs/video/acos-flujo.mp4)

*Pulsa la imagen para ver el video completo ([`docs/video/acos-flujo.mp4`](docs/video/acos-flujo.mp4), con subtítulos, sin audio).* Sigue un mismo proyecto desde que lo describes hasta que lo entregas: perfil o asistente → `acos init` → estado central → trabajo con el agente → gate con tu aprobación → 7 etapas → entregables.

**Contenido:** [Video](#míralo-en-82-segundos) · [Ejemplo e2e completo](docs/acos/ejemplo-e2e.md) · [Qué necesitas](#1-qué-necesitas-para-empezar) · [Qué obtienes al final](#2-qué-obtienes-al-final) · [Las 7 etapas](#3-las-7-etapas-en-lenguaje-simple) · [Tu primer proyecto paso a paso](#4-tu-primer-proyecto-paso-a-paso) · [Ver un proyecto ya terminado](#5-ver-un-proyecto-ya-terminado) · [Trabajar con el agente](#6-trabajar-con-el-agente) · [Referencia](#referencia)

---

## 1. Qué necesitas para empezar

| Necesitas | Para qué | ¿Obligatorio? |
|---|---|---|
| **Python 3.11+** y [`uv`](https://docs.astral.sh/uv/) | Instalar la herramienta `acos` | Sí |
| **Claude Code** o **Codex** | El agente que trabaja dentro del proyecto. ACOS no lo instala | Sí, para trabajar; no para el demo |
| **Respuestas sobre tu proyecto** (decisión, éxito, datos, entregables…) | Crear el proyecto, contestando al asistente o con un archivo YAML | Sí |
| Tus datos (CSV, Excel, SQL…) | Se usan en las etapas de análisis, no al crear el proyecto | Al llegar a esa etapa |
| Una carpeta de skills ("Foundry") | Skills reutilizables para el agente. Sin ella funciona igual con pautas del OS | No |

**Lo que ACOS te pregunta al crear un proyecto.** Si ejecutas `acos init` sin más, un asistente te hace las preguntas **una por una, en secuencia** (unas 11 a 13, más algunas condicionales según tu caso: por ejemplo, si el problema es predictivo pregunta por labels y target; si hay datos, por temporalidad y entidades repetidas). Lo esencial se resume en estos 6 temas, y casi todo admite dejarse en blanco (lo que no respondas queda anotado como pregunta abierta; puedes omitir el nombre real del cliente):

1. ¿Qué decisión necesita tomar el cliente?
2. ¿Qué problema u oportunidad motiva el trabajo?
3. ¿Cómo se mediría el éxito?
4. ¿Quién decide y quién usa el resultado?
5. ¿Qué datos existen y qué restricciones hay (tiempo, presupuesto, privacidad)?
6. ¿Qué entregables se esperan (informe, memo de decisión, deck, business case…)?

**`--profile-file` es opcional.** Si ya tienes las respuestas por escrito, pásalas en un archivo YAML (`acos init demo --profile-file perfil.yaml`) y te saltas las preguntas; ACOS igual te muestra el resultado y pide tu confirmación. Si no, ejecuta solo `acos init demo` y contesta al asistente (ejemplo en el paso 1 de abajo).

### Instalación (una vez)

```bash
uv tool install agentic-consulting-os
acos --version        # 0.1.1
```

Alternativa desde este repo: `git clone https://github.com/davidrodriguez2712/flujo-consultor-ml.git && cd flujo-consultor-ml && uv tool install .`

---

## 2. Qué obtienes al final

Al cerrar un proyecto tienes **una carpeta autocontenida y trazable**, no solo un documento. Lo que hay dentro es lo que le entregas al cliente y lo que te permite defenderlo meses después.

| Entregable | Dónde queda | Para qué sirve |
|---|---|---|
| **Memo de decisión** | `decision/recommendation.md` | Qué recomiendas, con qué evidencia y bajo qué límites |
| **Informe analítico** | `validation/model_validation.md` | Método, resultados y limitaciones |
| **Contrato de entrega** | `delivery/delivery_contract.md` | Qué se entregó, a quién y con qué alcance |
| **Evidencia reproducible** | `analysis/` | Código, datos de entrada con hash y resultados para volver a ejecutar |
| **Runbook y cierre** | `handoff/runbook.md`, `handoff/closure.md` | Cómo usar y mantener lo entregado, y qué señales exigen revisión |
| **Registro de aprobaciones** | `.acos/state.yaml` | Quién aprobó cada etapa y con qué evidencia |

Estos nombres salen del [proyecto piloto terminado](#5-ver-un-proyecto-ya-terminado); los entregables concretos de tu proyecto dependen de lo que declares en la pregunta 6. El estado final de un proyecto bien cerrado es `COMPLETED` con `integrity: OK`.

---

## 3. Las 7 etapas en lenguaje simple

Cada etapa responde **una pregunta** y termina con un **gate**: una puerta que ACOS revisa y que **tú** abres con tu aprobación.

| # | Etapa | La pregunta que responde | Qué haces tú | Qué hace el agente |
|---|---|---|---|---|
| 1 | `discovery` | ¿Quién decide y qué acción cambiará? ¿Qué fuentes y restricciones hay? | Aportas el contexto | Ordena el contexto y detecta lo que falta |
| 2 | `framing` | ¿Qué se mide, en qué unidad, en qué horizonte y quién lo aprueba? | Defines decisión, KPI y dueño | Redacta el brief y lo contrasta contigo |
| 3 | `diagnosis` | ¿Los datos y la evidencia alcanzan para decidir? | Das acceso a los datos | Revisa calidad, claves y riesgos (p. ej. *leakage*) |
| 4 | `execution` | ¿El método responde a la decisión y se puede reproducir? | Apruebas el método | Ejecuta el análisis o modelo |
| 5 | `validation` | ¿Es sólido y útil para la decisión? ¿Qué límites cambian la conclusión? | Revisas resultados y límites | Audita y mide |
| 6 | `delivery` | ¿Qué recomiendas y qué afirma realmente la evidencia? | Apruebas la recomendación | Prepara memo e informe |
| 7 | `handoff` | ¿Quién mantiene y usa cada entregable? | Cierras el proyecto | Redacta runbook y cierre |

Puedes **empezar en cualquier etapa** (por ejemplo en `framing` si el contexto ya existe) y **volver atrás** si cambia la pregunta. No siempre hace falta un modelo: la ruta (análisis, experimento, modelo, investigación…) se elige según la decisión. Detalle en [`workflow/project-lifecycle.md`](workflow/project-lifecycle.md).

---

## 4. Tu primer proyecto paso a paso

Este recorrido usa un caso de ejemplo (*priorizar inspecciones de fraude eléctrico*) y **tarda unos 5 minutos**. Llegas hasta aprobar el primer gate (`framing`), que es el mismo ciclo que repetirás en cada etapa.

> **¿Prefieres verlo funcionar primero?** `bash examples/quickstart/run.sh /tmp/acos-demo` ejecuta los pasos 1 a 7 solo y muestra las salidas.

### Paso 1 — Describir el proyecto

**Dos formas, a elegir:**

- **Con el asistente (por defecto):** `acos init demo-fraude` y respondes en pantalla, una pregunta tras otra («¿Qué decisión necesita tomar el cliente?», «¿Cómo se mediría éxito?», «¿Quién decide y quién usa el resultado?», «Datos existentes…», «Entregables…», «Etapa actual…»). Es lo habitual cuando empiezas de cero.
- **Con un archivo:** si ya tienes las respuestas, escríbelas una vez en YAML. Es lo que usa este recorrido porque se puede repetir sin teclear.

Guarda esto como `fraude.yaml` (es el ejemplo [`examples/quickstart/fraud-profile.yaml`](examples/quickstart/fraud-profile.yaml)). Son las respuestas a las preguntas de arriba:

```yaml
schema_version: 1
project: { slug: fraud, name: fraud }
engagement:
  decision: Priorizar inspecciones de fraude eléctrico       # pregunta 1
  archetypes: [PREDICT, PRIORITIZE_SELECT, OPTIMIZE]          # tipo de problema
  current_stage: framing                                      # etapa donde empiezas
data: { sources: [csv], characteristics: { supervised: true, labeled: partial } }
deliverables: [decision_memo, business_case]                  # pregunta 6
runtimes: [codex, claude_code]                                # tu agente
```

### Paso 2 — Crear el proyecto

```bash
acos init demo-fraude --profile-file fraude.yaml    # o, sin archivo:  acos init demo-fraude
```

**Qué ves:** ACOS te enseña, *antes de escribir nada*, el perfil que entendió, cómo clasificó el problema (y por qué), qué módulos va a usar, qué capacidades tiene cubiertas y cuáles no, y la lista de archivos que va a crear. Te pide la ruta de tu Foundry (déjala vacía para continuar sin él) y que confirmes con `s`. **No hay modo automático: siempre confirmas tú.**

**Qué sale:** la carpeta `demo-fraude/` con el manual (`MANUAL.md`), el resumen del proyecto (`PROJECT.md`), las instrucciones del agente (`AGENTS.md`, `CLAUDE.md`), el backlog (`TASKS.md`), el registro de decisiones (`DECISIONS.md`) y una carpeta por etapa. Lo que ACOS no puede cubrir con una skill lo marca como **brecha** y usa una pauta del OS; nunca inventa capacidades.

### Paso 3 — Ver dónde estás y qué sigue

```bash
cd demo-fraude
acos status
```

```json
{ "stage": "framing", "status": "NOT_STARTED", "completed": [],
  "next_gates": ["framing"], "integrity": "OK" }
```

```bash
acos next
```

```json
{ "stage": "framing",
  "objective": "Definir decisión, owner, KPI, unidad y horizonte.",
  "questions": ["¿Qué se optimiza o mide?", "¿Cuál es la unidad y el horizonte?", "¿Quién aprueba alcance y KPI?"],
  "outputs": ["framing/framing.yaml"] }
```

**Cómo leerlo:** `status` dice dónde estás; `next` dice qué trabajo toca (objetivo, preguntas a resolver y el archivo que hay que producir: `framing/framing.yaml`). Ninguno modifica nada, puedes ejecutarlos las veces que quieras.

### Paso 4 — Probar el gate antes de terminar (verás que se bloquea)

```bash
acos validate --gate framing
```

```json
{ "status": "BLOCKED",
  "findings": [{ "code": "fields-missing",
                 "message": "framing/framing.yaml: completar owner, metric, unit, horizon" }] }
```

**Cómo leerlo:** el gate te dice exactamente qué falta. Sale con código `4` (bloqueado). Es lo esperado: el entregable todavía está en blanco.

### Paso 5 — Hacer el trabajo de la etapa

Abre `framing/framing.yaml` y complétalo (solo, o pidiéndoselo a tu agente, ver [sección 6](#6-trabajar-con-el-agente)):

```yaml
decision: Priorizar inspecciones de fraude eléctrico
owner: Gerencia de Pérdidas No Técnicas
metric: Recuperación de energía por inspección
unit: kWh recuperados por inspección
horizon: 90 días
```

### Paso 6 — Registrar tu aprobación

Cuando **hayas revisado el contenido** y estés de acuerdo, lo dejas escrito en `.acos/state.yaml`. El hash está en `.acos/manifest.yaml`, campo `profile_sha256`:

```yaml
gate_reviews:
  framing:
    decision: PASS
    reviewer: David            # quién aprueba
    evidence:
      - framing/framing.yaml   # qué revisó
    profile_sha256: <copia el valor de .acos/manifest.yaml>
```

### Paso 7 — Confirmar que el gate pasa

```bash
acos validate --gate framing
```

```json
{ "status": "PASS", "findings": [], "evidence": ["framing/framing.yaml"] }
```

Código `0`: etapa aprobada con evidencia y revisor registrados.

### Paso 8 — Avanzar y repetir

Para pasar a `diagnosis`, **tú** añades `framing` a `completed_stages`, cambias `current_stage` y actualizas `objective` en `.acos/state.yaml` (a propósito, no hay comando automático de avance). Luego vuelves al paso 3 con la etapa nueva: `acos next` → trabajo → `acos validate` → aprobación. Repites hasta `handoff`; entonces `acos status` muestra `COMPLETED`.

> **¿Quieres ver las 7 etapas completas?** Esta guía llega hasta el primer gate. El recorrido de **todas las etapas, con los archivos y extractos reales de un proyecto terminado**, está en [`docs/acos/ejemplo-e2e.md`](docs/acos/ejemplo-e2e.md).

> **Importante:** `PASS` significa «el entregable está completo y alguien lo revisó». **No** prueba que el análisis sea correcto: eso sigue siendo tu criterio profesional.

### Si algo falla

| Ves | Significa | Qué hacer |
|---|---|---|
| Código `4` / `BLOCKED` | Faltan campos o hay un problema de integridad | Lee `findings`; corrige el archivo que indica |
| Código `3` / `NEEDS_REVIEW` | Falta tu revisión registrada | Revisa el contenido y completa `gate_reviews` |
| El gate no pasa tras aprobar | Hash o evidencia incorrectos | Copia de nuevo `profile_sha256` del manifest; usa rutas relativas que existan |
| Código `2` | Entrada inválida | Revisa el YAML o el comando |

---

## 5. Ver un proyecto ya terminado

La mejor forma de entender el resultado final es abrir uno completo. [`pilots/churn-retencion-sintetico/`](pilots/churn-retencion-sintetico/) recorrió las 7 etapas con datos **100 % sintéticos** (priorizar 50 clientes al mes por riesgo de abandono) y cerró en `COMPLETED`.

```bash
cp -r pilots/churn-retencion-sintetico /tmp/piloto && cd /tmp/piloto
acos status                    # COMPLETED · 7 etapas · integrity OK
acos validate --gate handoff   # PASS
```

Para recorrerlo etapa por etapa, con extractos de cada archivo y la aprobación de cada gate, sigue la guía [**Ejemplo e2e**](docs/acos/ejemplo-e2e.md). Si prefieres ir directo, lee en este orden: `decision/recommendation.md` (la recomendación) → `validation/model_validation.md` (la evidencia) → `handoff/runbook.md` (cómo se usa) → `handoff/closure.md` (el cierre) → `.acos/state.yaml` (las aprobaciones). Otros pilotos: `retail-valor-90d-publico`, `retail-capacidad-semanal-publico`, `riesgo-credito-sintetico`. Un caso narrado y ficticio: [`examples/synthetic/card-activation.md`](examples/synthetic/card-activation.md).

---

## 6. Trabajar con el agente

Dentro del proyecto abre tu agente:

```bash
cd demo-fraude
claude        # o: codex
```

Primer mensaje sugerido:

> *Lee MANUAL.md y PROJECT.md. Ejecuta `acos status` y `acos next`. Propón un plan para la etapa actual y dime qué contexto te falta antes de empezar.*

Ciclo de trabajo en cada etapa:

1. **Leer el estado** (`acos status` / `acos next`).
2. **Definir la tarea** con entradas, salida esperada y criterio de aceptación.
3. **Hacerla** con el agente, dejando evidencia reproducible (código, datos con hash, supuestos).
4. **Validar** con `acos validate --gate <etapa>`.
5. **Revisar tú** el contenido y registrar la aprobación.
6. **Cerrar la sesión** actualizando `TASKS.md`, `STATE.md` y `DECISIONS.md`.

`AGENTS.md` contiene las instrucciones compartidas y `CLAUDE.md` es un puente mínimo. Las skills seleccionadas se copian a `.claude/skills/` o `.agents/skills/`; comprueba que tu agente las ve antes de invocarlas.

---

## Referencia

### Comandos

| Comando | Qué hace | ¿Escribe? |
|---|---|---|
| `acos init [nombre]` | Crea el proyecto con el asistente de preguntas secuenciales, o con `--profile-file` (opcional); muestra todo y pide confirmación | Solo tras confirmar |
| `acos status` | Etapa, estado, bloqueos, gates pendientes, integridad | No |
| `acos next` | Objetivo, preguntas, outputs y brechas de la etapa | No |
| `acos validate --gate <g>` | Revisa un gate sin avanzar el estado | No |

Códigos de salida: `0` correcto/PASS · `2` entrada inválida · `3` NEEDS_REVIEW · `4` BLOCKED · `130` cancelado. Un `acos status` exitoso **no** significa gate aprobado.

### Qué hay dentro del proyecto

```text
demo-fraude/
├── .acos/                 # lo canónico: perfil, módulos, estado y aprobaciones, manifest con hashes
├── MANUAL.md  PROJECT.md  # cómo operar y qué se decidió
├── AGENTS.md  CLAUDE.md   # instrucciones para el agente
├── STATE.md  TASKS.md  DECISIONS.md  CAPABILITIES.md
├── context/ framing/ analysis/ modeling/ validation/ delivery/ handoff/   # según etapas y módulos
└── playbooks/ workflow/   # guías copiadas; el proyecto no depende de este repo
```

La fuente de verdad es `.acos/*`; `STATE.md` y la cabecera de `MANUAL.md` son vistas. No edites los snapshots: si cambia el perfil o la composición, se crea un proyecto nuevo (la V1 no tiene *update*).

### Skills y Foundry

El **Foundry** es tu carpeta de skills reutilizables, **en la ubicación que prefieras**. ACOS busca por defecto en `./david-skill-foundry` y `~/david-skill-foundry`; si la tuya está en otro lugar, **escribe la ruta cuando `acos init` la pida** y se guarda por dispositivo. Solo se leen `experiments/skills/` y `stable/`. Si no hay una skill compatible, ACOS lo declara como *brecha* y usa una pauta del OS.

**Todas las skills están en estado `experimental`: revisa siempre lo que producen.** Por ejemplo, `detect-leakage` 0.2.x (auditoría de *data leakage*) tiene evidencia limitada: una ejecución nativa aceptable *con reservas*, sin comparación con baseline ni generalización demostrada. Detalle en [`docs/acos/validation/`](docs/acos/validation/) y [`docs/acos/implementation-record.md`](docs/acos/implementation-record.md).

### Estado y límites

- **ACOS 0.1.1** publicado en PyPI (licencia MIT). Verificado en macOS, Linux (Docker) y Windows x64/ARM64; probado con Claude Code y Codex ([matriz](docs/acos/release.md)).
- Que pasen los tests no prueba la eficacia de las skills ni la calidad de un análisis.
- `acos init --llm` es opcional, pide consentimiento y nunca recibe datos del cliente.
- Una carpeta o repo organiza el trabajo, pero no es una barrera de seguridad: aísla a cada cliente con controles de acceso reales.

### Desarrollo

```bash
uv sync --extra dev
uv run python -m pytest -q             # 264 tests
uv run python -m build --no-isolation  # wheel + sdist
```

### Mapa del repo

| Ruta | Contenido |
|---|---|
| [`AGENTIC_CONSULTING_OS.md`](AGENTIC_CONSULTING_OS.md) | Manual del método: principios, ciclo y rutas (`RESEARCH`, `ANALYSIS`, `EXPERIMENT`, `MODEL`, `BUILD`, `DELIVERY`, `PRODUCT_UI`) |
| `src/acos/` | Compilador y CLI |
| `workflow/`, `playbooks/`, `templates/` | Ciclo de vida, guías por ruta y plantillas que se copian al proyecto |
| `examples/` | Ejemplo e2e ejecutable y caso narrado |
| `pilots/` | Proyectos sintéticos de punta a punta |
| `evaluations/`, `docs/acos/validation/` | Evidencia de evaluación de skills y plataformas |
| `schemas/`, `operations/`, `tests/` | Schemas de auditoría, guía de herramientas y suite del compilador |

Documentación: [ejemplo e2e completo](docs/acos/ejemplo-e2e.md) · [instalación](docs/acos/installation.md) · [uso de un proyecto](docs/acos/project-usage.md) · [distribución y límites](docs/acos/release.md).

## Licencia

[MIT](LICENSE) © 2026 David Rodríguez.
