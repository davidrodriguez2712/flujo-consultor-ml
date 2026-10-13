Proyecto: Priorización comercial retail con datos públicos
Decisión: Proponer al inicio de cada mes hasta 100 clientes identificables para revisión comercial, ordenados por ventas positivas esperadas a 90 días.
Etapa inicial: discovery
Módulos: consulting_core, data_analysis, supervised_model, selection, executive_delivery
Capacidades y cobertura:
- problem-framing: partial — Sin skill operativa compatible
  Límites: Pauta del OS con revisión humana; no demuestra correctitud ni sustituye evidencia específica.
- evidence-synthesis: partial — Sin skill operativa compatible
  Límites: Pauta del OS con revisión humana; no demuestra correctitud ni sustituye evidencia específica.
- dataset-understanding: skill — Propósito y condiciones compatibles con política del catálogo
  Límites: 
# Propósito

Esta skill proporciona una **comprensión estructural y metodológica de un dataset
antes de comenzar el análisis o el modelado**.

El problema que resuelve: la comprensión inicial de los datos suele hacerse de forma
improvisada y se salta directamente a estadísticas descriptivas, gráficos,
tratamiento de missing, feature engineering o entrenamiento. Antes de esas
actividades quedan sin resolver preguntas fundamentales —qué representa una fila,
cuál es la unidad de observación, cuál es el target y cuándo se conoce, qué
información estaba disponible al momento de predecir, qué variables son posteriores
al evento, qué joins duplican registros—.

Una comprensión incorrecta en esta etapa produce errores (target leakage, temporal
leakage, granularidad mal definida, duplicación por joins, train/test contamination,
uso incorrecto de identificadores, mala interpretación del target) que **luego no son
visibles en las métricas del modelo**: el modelo puede tener métricas excelentes y
aun así ser inválido.

La skill establece primero una comprensión confiable de los datos y señala los
principales riesgos y preguntas abiertas. No decide que el dataset esté listo para
modelar.

# Cuándo usar

Usar esta skill cuando:

- se recibe un dataset desconocido o solo su estructura (columnas, tipos, muestra);
- se inicia un nuevo proyecto de Data Science supervisado;
- se recibe una tabla nueva o se incorpora una nueva fuente de información;
- se recibe una nueva versión de un dataset ya conocido;
- se hereda un proyecto creado por otra persona;
- no está clara la unidad de observación o la granularidad;
- no se conoce con certeza el target;
- existe información temporal y hay riesgo de usar información futura;
- existen múltiples tablas que podrían relacionarse entre sí;
- existe
- supervised-validation: skill — Propósito y condiciones compatibles con política del catálogo
  Límites: 
# Propósito

Esta skill proporciona el **diseño explícito y justificado de la estrategia de
validación** de un problema supervisado, antes del feature engineering dependiente
del tiempo y antes del entrenamiento.

El problema que resuelve: la estrategia de validación suele definirse demasiado
tarde o elegirse por conveniencia (`train_test_split`, `StratifiedKFold`, `KFold`,
cross-validation estándar) sin comprobar primero si representa cómo funcionará el
modelo en producción. Una estrategia incorrecta produce métricas optimistas aunque
no exista ningún error visible en el entrenamiento. Ocurre sobre todo cuando hay
datos temporales, múltiples registros de una misma entidad, eventos repetidos,
grupos relacionados, panel data, ventanas de observación, prediction horizons,
cambios de distribución, o cuando entrenamiento y scoring ocurren en momentos
distintos. También ocurre cuando la validación es técnicamente válida pero está
desconectada de la decisión real (evaluar globalmente cuando operacionalmente solo
importa el desempeño sobre los primeros K casos priorizados).

El problema no es únicamente elegir entre train/test o cross-validation. Es diseñar
una validación que represente correctamente cómo se genera la información, cuándo
se realiza la predicción, sobre qué entidades, para qué horizonte, bajo qué
restricciones y cómo se usará realmente el modelo.

Principio rector:

> La validación debe reproducir lo más fielmente posible la situación real en la
> que el modelo generará predicciones: qué información existe, en qué momento,
> sobre qué entidades y para qué decisión.

La skill **no ejecuta el split ni entrena modelos**. Produce un diseño: qué
estrategia se recomienda, por qué representa mejor el problema, qué alternativas se
descartan y con qué motivo, cómo cons
- leakage-audit: skill — Propósito y condiciones compatibles con política del catálogo
  Límites: 
# Propósito

Esta skill proporciona una **auditoría dedicada de data leakage** sobre el
proceso completo de construcción de datos y validación de un problema
supervisado.

El problema que resuelve: es posible construir modelos con métricas aparentemente
excelentes utilizando información que, directa o indirectamente, no estaría
disponible en el momento real de realizar la predicción. Ese leakage hace que el
modelo obtenga métricas artificialmente altas, parezca generalizar durante
validación, seleccione features aparentemente muy predictivas y luego falle en
producción o produzca conclusiones de negocio incorrectas.

El problema no se reduce a identificar columnas "sospechosas". Muchas formas de
leakage dependen de comprender cuándo se genera una variable, cuándo ocurre el
evento objetivo, cuándo se realiza la predicción, qué información conoce
realmente el sistema en ese momento, cómo se construyeron las features, cómo se
dividieron train y test, y cómo se ejecutaron transformaciones, agregaciones y
joins. La skill audita el pipeline y la estrategia de validación, no sólo la
lista de features.

Principio rector:

> El modelo solamente debería utilizar información que habría estado
> legítimamente disponible en el momento real de realizar la predicción.

La skill **no elimina variables** ni decide que un pipeline sea válido. Explica
cuál es el posible problema, por qué podría constituir leakage, qué evidencia
existe, qué información falta, cómo podría comprobarse y qué acción sería
recomendable.

# Cuándo usar

Usar esta skill cuando:

- se recibe un nuevo dataset y ya hay un target (o evento objetivo) definido;
- existen timestamps y múltiples observaciones por entidad;
- se construyen features temporales: lag features, rolling features,
  tendencias, acumulados;
- se
- feature-design: skill — Propósito y condiciones compatibles con política del catálogo
  Límites: 
# Propósito

Esta skill proporciona el **diseño explícito y justificado del feature engineering**
de un problema supervisado, antes del entrenamiento y del código de construcción.

El problema que resuelve: el feature engineering suele hacerse de forma oportunista
—por intuición, por correlaciones, por ejemplos de otros proyectos, por pruebas
rápidas en notebooks—. Esto omite familias de features potencialmente útiles porque
el análisis depende de lo que el Data Scientist recuerde probar, y a la vez produce
features redundantes, poco interpretables, irreproducibles, dependientes de
información futura, construidas con ventanas temporales incorrectas o incompatibles
con producción. También ocurre que se construyen features antes de haber definido la
unidad de observación, el prediction timestamp, la observation window, el horizonte,
las restricciones de leakage o la estrategia de validación; en ese caso una feature
puede parecer técnicamente correcta pero ser inválida en el escenario real de
inferencia.

El problema no es "crear más variables". Es diseñar features de manera sistemática,
justificable, reproducible y compatible con el momento real de predicción.

Principio rector:

> Cada feature debe estar atada a una hipótesis de negocio, a una fuente de datos
> concreta y a una ventana temporal válida, y debe poder recalcularse con la
> información disponible en el momento real de predicción.

La skill **no escribe el código de construcción ni entrena modelos**. Produce un
plan: qué familias de features tienen sentido y por qué, qué features concretas
proponer dentro de cada una, qué ventana usa cada una, si es válida en inferencia,
qué prioridad tiene y qué conjunto conviene probar primero contra el baseline.

# Cuándo usar

Usar esta skill cuando:

- ya se comprendió 
- operational-selection: partial — Sin skill operativa compatible
  Límites: Pauta del OS con revisión humana; no demuestra correctitud ni sustituye evidencia específica.
- executive-synthesis: partial — Sin skill operativa compatible
  Límites: Pauta del OS con revisión humana; no demuestra correctitud ni sustituye evidencia específica.
- Snapshot understand-dataset 0.1.0 [experimental] foundry:experiments/skills/understand-dataset sha256:6fa84b9cea6729a27c383507811ece060aca84c5c3396c8887de4cd9dccf2693
- Snapshot design-validation 0.1.0 [experimental] foundry:experiments/skills/design-validation sha256:ad3d59e9bfe164de64c92d0eeeb3a12d6d7af6b4091ef5362a16d703498a1aa9
- Snapshot detect-leakage 0.1.0 [experimental] foundry:experiments/skills/detect-leakage sha256:d193cc5b86f1045cf073783e1d5f9325cb4eb09ab263abe4fe08fcf22baa502f
- Snapshot build-features 0.1.0 [experimental] foundry:experiments/skills/build-features sha256:4a71bc2e619e763a1f87bc1c31af82f4442c29d5693428cbe4bb607754a3b7de
Archivos propuestos:
  .acos/manifest.yaml
  .acos/modules.yaml
  .acos/project-profile.yaml
  .acos/state.yaml
  .agents/skills/build-features/SKILL.md
  .agents/skills/design-validation/SKILL.md
  .agents/skills/detect-leakage/SKILL.md
  .agents/skills/understand-dataset/SKILL.md
  .claude/skills/build-features/SKILL.md
  .claude/skills/design-validation/SKILL.md
  .claude/skills/detect-leakage/SKILL.md
  .claude/skills/understand-dataset/SKILL.md
  AGENTS.md
  CAPABILITIES.md
  CLAUDE.md
  DECISIONS.md
  MANUAL.md
  PROJECT.md
  STATE.md
  TASKS.md
  analysis/analysis_plan.md
  analysis/selection_plan.md
  context/business_context.md
  data/data_contract.yaml
  decision/recommendation.md
  delivery/delivery_contract.md
  delivery/storyline.md
  evidence/findings.md
  framing/framing.yaml
  handoff/runbook.md
  modeling/model_brief.md
  playbooks/data-understanding-analysis.md
  playbooks/experiments-and-models.md
  playbooks/research-impact-delivery.md
  validation/model_validation.md
  workflow/capability-lifecycle.md
  workflow/execution-and-qa.md
  workflow/isolation-and-context.md
  workflow/project-lifecycle.md
Confirmar incluye uso provisional de los snapshots experimentales indicados; no los promueve.
