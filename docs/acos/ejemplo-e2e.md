# Ejemplo e2e: un proyecto completo, etapa por etapa

Esta guía recorre **un proyecto real de ACOS de principio a fin**: las 7 etapas, qué hace cada persona, qué archivo sale de cada una y cómo queda la aprobación. Es la continuación del recorrido corto del [README](../../README.md#4-tu-primer-proyecto-paso-a-paso) (que llega hasta el primer gate).

**Caso:** [`pilots/churn-retencion-sintetico/`](../../pilots/churn-retencion-sintetico/). Una empresa **ficticia** de suscripciones quiere decidir a qué 50 clientes activos contactar cada mes para retenerlos. Datos 100 % sintéticos; no hay conclusiones sobre clientes reales.

> **Cómo leer esta guía.** Es una *lectura guiada* de un proyecto terminado, no un script que se ejecute solo: el trabajo de las etapas lo hizo un agente en sesiones anteriores, con David Rodríguez como revisor. Todos los extractos son del piloto. Para explorarlo tú mismo:
>
> ```bash
> cp -r pilots/churn-retencion-sintetico /tmp/piloto && cd /tmp/piloto
> acos status                     # COMPLETED · integrity OK
> acos validate --gate framing    # PASS (cambia el nombre del gate para ver cada etapa)
> ```
> Verificado en una copia: los 7 gates (`discovery`, `framing`, `diagnosis`, `execution`, `validation`, `delivery`, `handoff`) dan `PASS`.

## El mapa en una tabla

| Etapa | Pregunta | Qué sale (archivo) | Aprobado con |
|---|---|---|---|
| 1 `discovery` | ¿Quién decide y qué acción cambiará? | `context/business_context.md` | contexto, informe y aprobación |
| 2 `framing` | ¿Qué se mide, en qué unidad y horizonte? | `framing/framing.yaml`, `validation/validation_design.md` | contrato + protocolo temporal |
| 3 `diagnosis` | ¿Los datos alcanzan? ¿Hay leakage? | `evidence/findings.md`, `reports/dataset/…`, `reports/leakage/…` | hallazgos y auditorías |
| 4 `execution` | ¿El método responde y se reproduce? | `reports/baseline/development-….md` | baseline + auditoría de leakage |
| 5 `validation` | ¿Es sólido? ¿Qué límites cambian la conclusión? | `validation/model_validation.md` | evaluación con datos apartados |
| 6 `delivery` | ¿Qué se recomienda y qué afirma la evidencia? | `decision/recommendation.md`, `delivery/delivery_contract.md` | memo + contrato |
| 7 `handoff` | ¿Quién mantiene y usa los entregables? | `handoff/runbook.md`, `handoff/closure.md` | runbook + cierre |

Además de los gates de etapa, el piloto registra **revisiones por módulo** (`data-quality`, `data_analysis-review`, `supervised_model-review`, `selection-review`, `executive_delivery-review`): 12 gates en total, todos con revisor y evidencia en `.acos/state.yaml`.

**El patrón de cada etapa es el mismo:** `acos next` → el agente trabaja → `acos validate` → **tú revisas** → se registra la aprobación en `.acos/state.yaml` y en `evidence/approvals/<fecha>-<etapa>.md` → pasas a la siguiente.

---

## 0. Crear el proyecto

El perfil (`.acos/project-profile.yaml`) recoge las respuestas a las [6 preguntas](../../README.md#1-qué-necesitas-para-empezar):

```yaml
project: { slug: churn-retencion-sintetico, client: Empresa ficticia de suscripciones, … }
engagement:
  decision: Proponer qué clientes activos priorizar para revisión de retención cada mes.
  success_metric: 'Propuesta: Precision@50 mensual y valor en riesgo; impacto causal de retención no identificado.'
  archetypes: [DIAGNOSE, PREDICT, PRIORITIZE_SELECT]
  current_stage: discovery
data: { sources: [csv], characteristics: { supervised: true, labeled: partial, temporal: true } }
constraints:
  - Datos 100% sintéticos, seed 20261007; no conclusiones sobre clientes reales.
  - 'Capacidad operativa propuesta: 50 contactos por mes; pendiente de revisión.'
```

Observa dos cosas: el éxito está declarado como *propuesta* (nada se da por acordado) y `open_questions` deja anotado lo que falta confirmar. Se crea con `acos init … --profile-file`.

---

## 1. `discovery` — Entender el contexto

**Pregunta:** ¿Quién decide y qué acción cambiará? ¿Qué fuentes y restricciones hay?

- **Tú:** aceptas o ajustas la decisión, la capacidad (50 contactos/mes), el KPI y la definición de churn; designas al revisor.
- **Agente:** ordena el contexto y deja las definiciones por escrito para que las apruebes.
- **Sale:** `context/business_context.md`.

Extracto (así separa lo propuesto de lo aprobado):

> *Cada comienzo de mes, proponer qué clientes activos priorizar… Supuesto operativo: capacidad de 50 contactos/mes. […] Estos son supuestos de laboratorio propuestos por el asistente, no instrucciones de una empresa real.*
>
> *Revisión de discovery — 2026-10-07: David aceptó las definiciones presentadas y actuar como reviewer. K=50, churn y Precision@50/Recall@50 aceptados. Discovery PASS.*

**Gate** `discovery` → evidencia: `context/business_context.md`, `PILOT_REPORT.md`, `evidence/approvals/2026-10-07-discovery.md`.

---

## 2. `framing` — Enmarcar la decisión

**Pregunta:** ¿Qué se optimiza o mide? ¿Cuál es la unidad y el horizonte? ¿Quién aprueba?

- **Tú:** apruebas el contrato y el diseño de validación.
- **Agente:** redacta `framing/framing.yaml` y el protocolo temporal.
- **Sale:** `framing/framing.yaml`, `framing/metrics.md`, `validation/validation_design.md`.

```yaml
decision: Priorizar 50 clientes activos por mes para revisión de retención.
metric:
  primary: Precision@50 por mes
  secondary: [Recall@50 por mes, Lift@50 por mes]
  business_context: MRR en riesgo; no es margen, recupero ni ROI incremental
unit: cliente activo × comienzo de mes calendario
horizon: Cancelación en [inicio del mes de scoring, inicio del mes siguiente)
capacity: 50
tie_break: customer_id ascendente, sin usarlo como predictor
```

Es exactamente el [`framing.yaml` del paso 5 del README](../../README.md#paso-5--hacer-el-trabajo-de-la-etapa), pero completo. Fíjate en la nota del KPI: dice qué **no** significa (no es ROI).

**La aprobación queda por escrito**, con la pregunta y la respuesta (`evidence/approvals/2026-10-07-framing.md`):

> *Pregunta: «¿Apruebas el contrato y este protocolo temporal para continuar?» — Respuesta del usuario: «si apruebo». Alcance: aprobación de framing y de ese diseño temporal. No aprueba outputs de diagnóstico todavía no producidos, ejecución ni performance de un modelo.*

**Gate** `framing` → 4 evidencias (`framing.yaml`, `metrics.md`, `validation_design.md`, aprobación).

---

## 3. `diagnosis` — ¿Los datos alcanzan?

**Pregunta:** ¿Qué hipótesis tienen evidencia? ¿Qué falta para decidir?

- **Tú:** das acceso a los datos (aquí, sintéticos y reproducibles) y revisas los hallazgos.
- **Agente:** audita calidad, claves y riesgos; usa las skills experimentales `understand-dataset` y `detect-leakage`.
- **Sale:** `evidence/findings.md`, `reports/dataset/dataset-understanding-…md`, `reports/leakage/leakage-audit-…md`, `data/data_contract.yaml`.

Extracto de `evidence/findings.md`: hechos separados de límites.

> *[Hecho] 35 990 snapshots sobre 24 períodos; claves sin duplicados. · [Hecho] 35 018 labels observadas y 972 pendientes; estas últimas están vacías. · [Hecho] El join directo de tickets produciría 36 853 filas frente a 35 990 snapshots: agregar antes del join. · [Límite] Sin datos reales ni tratamiento/control: no extrapolar tasa, ranking o impacto.*

**Aquí el flujo encontró un problema real.** La auditoría de leakage marcó un hallazgo *Crítico — Confirmado y corregido*: la exportación incluía una cancelación posterior al corte (una fila en la versión 1, cero en la 2). La primera versión de los datos **se conservó archivada, no se borró**, y se generó la v2 con 26 checks sin infracciones. También dejó riesgos *condicionados al uso* y límites *no determinables* (por ejemplo, no se puede declarar auditado un pipeline de entrenamiento que aún no existe).

> Esta etapa muestra por qué el gate pide revisión humana: un `PASS` automático no habría detectado que había que decidir qué hacer con el dato defectuoso.

**Gates** `diagnosis` y `data-quality`.

---

## 4. `execution` — Ejecutar el método

**Pregunta:** ¿El método responde a la decisión? ¿Se puede reproducir cada output?

- **Tú:** apruebas el método antes de ver resultados.
- **Agente:** construye un baseline sencillo (modelo por grupos con cuatro señales históricas), con la política fijada **antes** de ejecutar y sin tuning; nueve folds walk-forward.
- **Sale:** `reports/baseline/development-….md`, `analysis/baseline.py`, `modeling/model_brief.md`, una segunda auditoría de leakage sobre el código ya existente.

| Métrica, media mensual | Baseline | Aleatorio esperado |
|---|---:|---:|
| Precision@50 | 13.56 % | 3.85 % |
| Recall@50 | 10.74 % | 3.13 % |

El informe lo dice sin adornos: *«Revisión humana pendiente»*. Hasta que apruebas, no es un resultado aceptado.

**Gate** `execution` → 4 evidencias, incluida `analysis/outputs/baseline-audit.json` (hashes y recálculos).

---

## 5. `validation` — Medir sin hacerse trampa

**Pregunta:** ¿Se evita leakage o inferencia causal no identificada? ¿Qué límites cambian la decisión?

- **Tú:** revisas resultados **y** límites.
- **Agente:** evalúa el modelo **congelado** sobre seis meses apartados (julio–diciembre 2025), sin reentrenar ni ajustar.
- **Sale:** `validation/model_validation.md`, `analysis/outputs/holdout-audit.json`.

| Métrica, media mensual | Desarrollo (9 meses) | Holdout (6 meses) | Aleatorio esperado |
|---|---:|---:|---:|
| Precision@50 | 13.56 % | 10.67 % | 4.28 % |
| Lift@50 | 3.49 | 2.52 | 1.00 |

Lo importante es lo que dice el informe sobre la caída: *«La comparación no identifica la causa: los meses, población y prevalencia difieren […]. No atribuir…»*. Se describe la variación mensual, no solo la media, y no se inventa una explicación.

**Gates** `validation` y las revisiones por módulo (`data_analysis-review`, `supervised_model-review`, `selection-review`).

---

## 6. `delivery` — Recomendar con límites

**Pregunta:** ¿Qué opción se recomienda y bajo qué condiciones? ¿Qué afirma realmente la evidencia?

- **Tú:** apruebas la recomendación y lo que se promete.
- **Agente:** redacta el memo de decisión, la historia (`delivery/storyline.md`) y el contrato de entrega.
- **Sale:** `decision/recommendation.md`, `delivery/delivery_contract.md`, `delivery/delivery-manifest.json`.

La decisión propuesta es deliberadamente prudente:

> *Aceptar el ranking como resultado analítico del laboratorio y como referencia para un futuro piloto con datos reales. Antes de justificar una campaña o inversión, validar disponibilidad de datos y desempeño en el contexto real, definir la intervención y comprobar su efecto incremental.*

La historia (`storyline.md`) termina con una regla clave: *«Sin ROI, ahorro, margen recuperado o uplift inventados.»* El contrato de entrega lista cada artefacto, su ruta y su función (memo, informe, especificación, plan de selección, evidencia, auditorías, código, datos).

**Gates** `delivery` (5 evidencias) y `executive_delivery-review`.

---

## 7. `handoff` — Cerrar y transferir

**Pregunta:** ¿Quién mantiene y usa cada entregable? ¿Qué señales requieren revisión?

- **Tú:** cierras el proyecto.
- **Agente:** redacta el runbook y el balance de cierre, y verifica que lo reproducible se reproduce.
- **Sale:** `handoff/runbook.md`, `handoff/closure.md`, `handoff/capability_feedback.md`, `handoff/handoff-manifest.json`.

Extracto de `handoff/closure.md`:

> *Discovery → framing → diagnosis → execution → validation → delivery → handoff. Siete etapas y doce gates aprobados con evidencia. […] Cuatro CSV y cinco JSON de desarrollo reproducidos idénticos; hashes originales conservados. El test no se repitió al preparar handoff. […] La aprobación corresponde al laboratorio. No hay beneficio causal, ROI, generalización real o producción demostrados.*

Y el estado final, que puedes comprobar tú mismo:

```bash
acos status
```

```json
{ "project": "Piloto sintético de churn y retención", "stage": "handoff", "status": "COMPLETED",
  "completed": ["discovery","framing","diagnosis","execution","validation","delivery","handoff"],
  "total_stages": 7, "next_gates": [], "integrity": "OK", "findings": [] }
```

`acos next` responde *«Proyecto completado; no hay una siguiente etapa»*. Si el cierre fuera inconsistente, `integrity` pasaría a `BLOCKED` y los comandos devolverían código `4`.

---

## Qué aprender de este ejemplo

1. **Lo propuesto y lo aprobado se mantienen separados.** El agente propone; tú apruebas, y la aprobación queda en un archivo con fecha, pregunta y respuesta.
2. **Cada afirmación tiene un límite al lado.** «Precision@50 de 10,67 %» siempre viene con «no hay beneficio causal».
3. **Los problemas se conservan, no se esconden.** La v1 defectuosa de los datos quedó archivada.
4. **El resultado es una carpeta que alguien más puede abrir meses después** y entender qué se hizo, por qué y con qué evidencia.
5. **Las skills son experimentales.** `understand-dataset` y `detect-leakage` ayudaron, pero el propio piloto aclara que no hubo revisión independiente ni evaluación comparativa de ellas.

## Límites de este ejemplo

- Es sintético y de laboratorio: no demuestra rendimiento con datos reales ni impacto en negocio.
- David actúa como revisor de todos los gates y también como responsable del laboratorio; en un proyecto real serían roles distintos.
- Los nombres de archivos dependen de los módulos que ACOS compone según tu perfil; otro proyecto puede producir otros.
- Para ver el mismo flujo en otro dominio, están `pilots/riesgo-credito-sintetico/`, `retail-valor-90d-publico/` y `retail-capacidad-semanal-publico/`.

Siguiente lectura: [uso de un proyecto](project-usage.md) · [instalación](installation.md) · [manual del método](../../AGENTIC_CONSULTING_OS.md).
