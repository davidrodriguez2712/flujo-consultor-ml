---
name: build-features
description: >-
  Diseña un plan de feature engineering condicionado al contexto ANTES de entrenar.
  Parte del objetivo de negocio, la unidad de observación, el target, el prediction
  timestamp, la observation window, el prediction horizon, la estrategia de
  validación, las restricciones de leakage y las columnas disponibles, y recorre de
  forma sistemática las familias de features potencialmente relevantes: raw,
  transformaciones numéricas, categóricas, temporales (lag, rolling, EWMA,
  tendencias, slopes, recencia, streaks, acumulados, estacionalidad), de
  comportamiento, relativas (entidad frente a su historia, su grupo o sus peers),
  históricas de eventos, geoespaciales, de red/grafo y domain-specific. Para cada
  feature exige una hipótesis de negocio, los inputs, la ventana temporal válida, la
  viabilidad en inferencia, el riesgo de leakage, la prioridad (P0 / P1 / P2) y el
  coste de implementación. Produce un reporte con la feature strategy, un feature
  inventory, el contrato temporal, la priorización, las leakage notes, el plan de
  implementación, el feature lineage, el esquema del dataset modelable, las preguntas
  abiertas y el siguiente conjunto de features a probar contra el baseline.
  NO escribe el código de construcción, NO entrena ni optimiza modelos, NO hace
  feature selection, NO crea features solo porque sean técnicamente posibles y NO
  inventa familias (lags / rolling, geoespaciales, de grafo) cuando los datos no las
  soportan.
  Úsala tras comprender el dataset, revisar el leakage y diseñar la validación, antes
  del entrenamiento, al incorporar nuevas fuentes de datos, al intentar mejorar un
  baseline o al revisar un feature set existente; no la uses para la comprensión
  estructural inicial (usa `understand-dataset`), para auditar un pipeline o un
  conjunto de features ya construidos (usa `detect-leakage`), para diseñar la
  estrategia de validación (usa `design-validation`), ni cuando la tarea es
  seleccionar qué features conservar o entrenar modelos.
status: experimental
version: 0.1.0
domain: data-science
---

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

- ya se comprendió el dataset, se revisó el leakage y se diseñó la validación, y
  falta decidir qué features construir;
- antes de entrenar o comparar modelos;
- se incorpora una nueva fuente de datos o se reciben nuevas variables;
- se quiere mejorar un baseline con features incrementales;
- se necesita diseñar features temporales (lag, rolling, tendencias, acumulados) sin
  leakage;
- se quiere traducir conocimiento de negocio en variables modelables;
- se necesita revisar un feature set existente y decidir cuáles tienen sentido
  conservar por hipótesis y viabilidad (no por importancia estadística).

Ejemplos de disparador:

> Diseña features para este problema usando solo información disponible antes del
> scoring.

> Propón feature engineering para este panel cliente-mes.

> Construye un plan de variables temporales sin leakage.

> Revisa estas features y dime cuáles tienen sentido.

> Genera un plan de features a partir de este problema de fraude.

> Tenemos los datos de EQUANS. Diseña las familias de features que deberíamos probar
> primero.

# Cuándo NO usar

No utilizar esta skill cuando:

- lo que se necesita es la **comprensión estructural inicial** del dataset (unidad de
  observación, claves, granularidad, target candidato, calidad básica): usar
  `understand-dataset`;
- lo que se necesita es **auditar el data leakage** de un conjunto de features, un
  pipeline o un código de feature engineering ya construido: usar `detect-leakage`.
  Esta skill diseña las features y su contrato temporal; `detect-leakage` comprueba
  si una implementación concreta lo respeta;
- lo que se necesita es **diseñar la estrategia de validación** (qué split, qué
  cross-validation, out-of-time, manejo de entidades): usar `design-validation`;
- la tarea pedida es hacer **feature selection**: decidir qué variables conservar a
  partir de importancia, correlación con el target, estabilidad o coste es un
  problema relacionado pero distinto de generar y diseñar features;
- la tarea pedida es entrenar, comparar, seleccionar u optimizar un modelo;
- no hay **nada sobre lo que razonar**: ni estructura del dataset, ni target, ni
  prediction timestamp, ni columnas disponibles.

# Inputs

## Obligatorios

- La **estructura del problema**: unidad de observación, entity ID, columna de fecha
  (si existe), target y granularidad (aunque sean provisionales).
- La **lista de columnas disponibles** con su tipo (y, si es posible, cardinalidad y
  proporción de missing).

Idealmente también, como salida de las skills previas:

- **prediction timestamp** y qué información existe legítimamente en ese instante;
- **observation window** y **prediction horizon**;
- la **estrategia de validación** ya diseñada (define los límites dentro de los que
  puede ajustarse cualquier transformación).

## Opcionales

- Dataset inspeccionable (CSV, Parquet, Excel, JSON, DataFrame en memoria).
- Variables prohibidas y **leakage findings** previos (`detect-leakage`,
  `understand-dataset`).
- Label delay, frecuencia de scoring y de reentrenamiento.
- Contexto de negocio: proceso, evento de interés, hipótesis conocidas, e
  información realmente disponible durante el scoring.
- Research previo: enfoques de literatura, features usadas en benchmarks, buenas
  prácticas del dominio.
- Feature set existente: lista de features, código de construcción, importancia,
  métricas, problemas conocidos.
- Coordenadas o zonas (para valorar features geoespaciales).
- Estructura relacional o de grafo (para valorar features de red).
- Políticas de confidencialidad, almacenamiento y procesamiento del proyecto (p. ej.
  las condiciones de datos de EQUANS).
- Ruta de salida del reporte: si se indica, se usa en lugar de la ruta por defecto
  (`reports/features/feature-plan-<YYYY-MM-DD>.md`).

Cuando falte el prediction timestamp, una ventana, o la semántica de negocio de una
columna, marcar el punto como **No determinable** y llevarlo a "Preguntas abiertas".
No inventar timestamps, ventanas ni significados.

# Preconditions

Antes de ejecutar el workflow debe ser cierto:

- Existe un target o evento objetivo, aunque sea provisional.
- Existe la lista de columnas disponibles con su tipo.
- Se conoce, o se puede asumir de forma provisional y declarada, el momento de
  predicción y qué información existe legítimamente en él.
- Está permitido procesar los datos de acuerdo con las políticas del proyecto.

Recomendable: `understand-dataset`, `detect-leakage` y `design-validation` ya se
ejecutaron. Si no, la skill puede continuar, pero debe declarar los supuestos que
está asumiendo y llevarlos a "Preguntas abiertas".

# Workflow

## 1. Comprender el problema

- Fijar: objetivo de negocio, unidad de observación, entidad y target.
- Fijar el **prediction timestamp**: el instante en que el modelo decide y qué
  información existe legítimamente en ese instante. Para EQUANS: el momento de
  priorizar qué suministro inspeccionar, antes de la inspección.
- Situar el evento objetivo en la línea temporal del proceso de negocio y anotar el
  **label delay** y el **prediction horizon**.
- Recoger las **hipótesis de negocio** conocidas sobre qué comportamientos
  discriminan el target.
- Anotar el contexto que falta (definición del positivo, ventanas, información
  disponible en scoring). No inventarlo: pasa a "Preguntas abiertas".

## 2. Analizar los inputs

- Construir un **inventario de columnas**. Por cada columna: tipo, cardinalidad,
  proporción de missing y **rol** (entity ID / fecha / target / candidata a feature /
  prohibida por leakage findings previos).
- Determinar, **con evidencia en los datos y no por suposición**, qué estructuras
  existen:
  - **temporal / panel** (`entidad × período`): ¿hay columna de fecha? ¿cuántas
    observaciones por entidad? ¿cobertura y huecos?
  - **relacional / grafo**: ¿existen columnas que definan relaciones entre entidades
    (aristas, referencias)?
  - **geoespacial**: ¿existen coordenadas o códigos de zona válidos?
- Incorporar los **leakage findings** y las **variables prohibidas** previas: esas
  columnas no pueden ser inputs de ninguna feature.

## 3. Ejecutar el procedimiento

Recorrer de forma **sistemática** las familias de features y, por cada familia
**aplicable a este dataset**, proponer features concretas:

- **Raw**: variables originales utilizables sin transformación.
- **Transformaciones numéricas**: log, clipping, winsorization, ratios, diferencias,
  normalizaciones relativas.
- **Categóricas**: agrupaciones, flags, interacciones, frecuencia de categoría,
  rare-category handling.
- **Temporales** (solo si hay estructura temporal): lags, rolling statistics, EWMA,
  tendencias, slopes, variaciones, cambios porcentuales, recencia, frecuencia,
  streaks, acumulados, estabilidad, volatilidad, estacionalidad.
- **Comportamiento**: intensidad, frecuencia, desviación respecto al comportamiento
  histórico, cambios estructurales, consistencia, patrones recientes.
- **Relativas**: comparar la entidad contra su propia historia, su grupo, su
  segmento, su zona o peers comparables.
- **Históricas de eventos** (si son válidas): número de eventos previos, tiempo desde
  el último evento, frecuencia histórica, reincidencia.
- **Geoespaciales** (solo si hay coordenadas/zonas): densidad, distancia, riesgo
  local, vecinos, clusters espaciales.
- **De red / grafo** (solo si hay topología válida): grado, neighborhood statistics,
  riesgo de nodos cercanos, agregaciones por red.
- **Domain-specific**: derivadas del conocimiento del proceso de negocio.

**Descartar explícitamente y con motivo** las familias que los datos no soportan
(sin fechas → no lags ni rolling; sin coordenadas → no geoespaciales; sin topología →
no grafo).

Para **cada feature propuesta** registrar:

- **hipótesis** de negocio (qué señal se espera capturar);
- **inputs** (columnas fuente);
- **ventana temporal** utilizada;
- **viabilidad en inferencia**: Válida / Válida con condiciones / Inválida / No
  determinable;
- **riesgo de leakage**;
- **prioridad**: P0 / P1 / P2;
- **coste** de implementación.

Construir el **contrato temporal**: para prediction time = `t`, qué períodos son
inputs válidos (`t-1`, `t-2`, …) y cuáles inválidos (`t`, `t+1`), y qué regla aplica
a cada tipo de agregación (lag, rolling, EWMA, acumulados, tendencias).

## 4. Verificar el resultado

- Recorrer la checklist de "Verificación final".
- Ejecutar los checks deterministas disponibles y registrar su resultado en el
  reporte.
- **Revisar falsos positivos**:
  - no proponer una feature sin hipótesis clara solo para aumentar la cantidad;
  - no proponer una familia sin soporte en los datos (geoespacial sin coordenadas,
    grafo sin topología, temporal sin fechas);
  - detectar **redundancia**: features casi idénticas → consolidar en una;
  - comprobar que cada feature temporal respeta el contrato temporal;
  - comprobar la **viabilidad en producción**: los inputs de cada feature deben
    existir en el momento de scoring.

## 5. Construir el output

- Redactar el plan con la estructura de la sección "Output".
- **No** escribir el código de construcción. **No** proponer modelo, algoritmo ni
  hiperparámetros. **No** hacer feature selection.
- **Persistir el reporte** como archivo `.md` en
  `reports/features/feature-plan-<YYYY-MM-DD>.md` (fecha real de ejecución; crear la
  carpeta `reports/features/` si no existe). No sobrescribir: si ya existe un archivo
  con esa fecha, añadir sufijo `-02`, `-03`, … Si el usuario indicó una ruta de
  salida, usar esa.
- Encabezar el archivo con el frontmatter de trazabilidad (ver "Output"): skill,
  versión, fecha real, proyecto si se conoce, inputs analizados —con `sha256` cuando
  sean archivos locales— y una línea de estado.
- Respetar las políticas de confidencialidad del proyecto: no volcar en el archivo
  datos sensibles, PII ni muestras de registros más allá de lo imprescindible como
  evidencia (relevante para EQUANS).
- Devolver al usuario un resumen breve **y la ruta del archivo escrito**.

# Checks deterministas

Siempre que sea posible, utilizar evidencia determinista antes de realizar
inferencias. Ejecutar estas comprobaciones ad hoc sobre los datos o el código
(p. ej. con pandas / scikit-learn); **no** crear scripts en `scripts/` para esto
(ver `AGENTS.md` → "# Simplicidad").

Checks disponibles:

- **Existencia y tipo de las columnas fuente** de cada feature propuesta:
  `col in df.columns` y dtype esperado. Una feature cuyos inputs no existen no puede
  proponerse.
- **Soporte de estructura**:
  - antes de proponer lags / rolling: nº de observaciones y cobertura temporal por
    entidad (`df.groupby(id)['fecha'].agg(['count', 'min', 'max'])`); con 1–2
    observaciones por entidad, las features temporales no son viables;
  - antes de proponer geoespaciales: presencia y validez de columnas de coordenadas
    o zona (rango plausible, proporción de missing);
  - antes de proponer grafo: presencia de columnas que definan relaciones/aristas.
- **Contrato temporal de agregaciones**: para cada feature con ventana, comprobar que
  las fechas incluidas son estrictamente anteriores al prediction timestamp
  (`< t`, o `<= t-1` según granularidad). Una ventana que incluye `t` o `t+1` es
  inválida.
- **Missing y cobertura de la feature propuesta**: `df[cols].isna().mean()` sobre las
  columnas fuente; una feature cuya base tiene cobertura muy baja se degrada a P2 o se
  marca como Válida con condiciones.
- **Redundancia entre features propuestas**: correlación / near-duplication
  (`.corr()` sobre un cálculo rápido de las candidatas); pares casi idénticos →
  consolidar.
- **Señal univariante como indicio de leakage** (indicio, no prueba): correlación o
  AUC univariante de una feature sospechosa frente al target; un valor casi perfecto
  refuerza la sospecha pero no la confirma por sí solo.
- **Viabilidad en producción**: para cada feature, ¿sus inputs existen en el momento
  de scoring con la latencia real? Marcar las que dependen de información solo
  disponible en análisis offline.

# Reglas

La skill debe:

- atar **cada feature** a: hipótesis de negocio, inputs, ventana temporal, viabilidad
  en inferencia, riesgo de leakage, prioridad y coste;
- recorrer **sistemáticamente** todas las familias de features y **descartar con
  motivo** las que los datos no soportan;
- construir un **contrato temporal explícito** (inputs válidos vs inválidos respecto
  al prediction timestamp);
- **priorizar** las features (P0 / P1 / P2) en lugar de listarlas todas por igual;
- preferir los checks deterministas antes que las inferencias basadas en el nombre de
  una columna;
- declarar **No determinable** cuando falte el prediction timestamp, una ventana o la
  semántica de negocio, y llevar el punto a "Preguntas abiertas";
- mantener siempre el vínculo **feature ↔ hipótesis de negocio**.

La skill no debe:

- escribir el código de construcción de las features;
- entrenar, comparar, seleccionar u optimizar modelos;
- hacer **feature selection** (decidir qué variables conservar a partir de
  importancia o métricas);
- crear features solo porque son técnicamente posibles;
- inventar familias de features sin soporte en los datos (lags sin fechas,
  geoespaciales sin coordenadas, grafo sin topología);
- generar decenas o cientos de variables sin priorización (feature explosion);
- proponer múltiples transformaciones casi idénticas;
- asumir la semántica de una columna únicamente por su nombre;
- diseñar features que se calculen sobre todo el dataset ignorando los límites de la
  estrategia de validación;
- optimizar el feature engineering para maximizar el score de una hackathon o
  competición en lugar de representar producción.

# Output

El reporte se entrega en dos formas: (a) un resumen en la respuesta al usuario; (b)
un archivo `.md` persistido en `reports/features/feature-plan-<YYYY-MM-DD>.md` (o la
ruta indicada por el usuario), encabezado con el frontmatter de trazabilidad. El
archivo es la fuente de trazabilidad; su contenido bajo el frontmatter usa la
estructura de esta sección.

Frontmatter de trazabilidad del archivo:

```yaml
---
skill: build-features
version: 0.1.0
fecha: <YYYY-MM-DD>
proyecto: <slug si se conoce; si no: (sin especificar)>
inputs:
  - <ruta o descripción del input>   # sha256:<hash> si es un archivo local
estado: <resumen de una línea del resultado>
---
```

El cuerpo del reporte debe utilizar la siguiente estructura:

## Resumen

- Familias de features recomendadas (una frase).
- Principal precaución o limitación.
- ¿Es posible un plan fiable con la información disponible, o depende de confirmar
  preguntas abiertas?

## Contexto de features

Objetivo, unidad de observación, target, prediction timestamp, observation window,
prediction horizon y estrategia de validación asumida. Solo lo relevante para el
feature engineering. Marcar explícitamente lo que se está asumiendo.

## Feature strategy

Qué familias de features tienen sentido para este problema y por qué. Qué familias se
descartan y por qué (sin fechas, sin coordenadas, sin topología, sin hipótesis
razonable).

## Feature inventory

Tabla:

| Feature | Familia | Hipótesis | Inputs | Ventana | Viabilidad | Riesgo leakage | Prioridad | Coste |
|---|---|---|---|---|---|---|---|---|

Viabilidad ∈ {Válida, Válida con condiciones, Inválida, No determinable}.

## Contrato temporal

Para prediction time = `t`: qué períodos son inputs válidos (`t-1`, `t-2`, …) y
cuáles inválidos (`t`, `t+1`). Regla por tipo de agregación (lag, rolling, EWMA,
acumulados, tendencias, slopes).

## Priorización

- **P0** — implementar primero.
- **P1** — implementar si los datos lo permiten.
- **P2** — explorar si hay tiempo o evidencia.

Indicar el criterio con que se asignó la prioridad (hipótesis fuerte + bajo coste +
alta viabilidad → P0).

## Leakage notes

Riesgos derivados de cada construcción: rolling / trends / aggregates / EWMA /
cumulative con información futura, ventana incorrecta, cálculo antes del split. Nota:
la auditoría detallada de un pipeline concreto corresponde a `detect-leakage`.

## Plan de implementación

Qué transformaciones deberían implementarse y en qué orden, a nivel de
**especificación** (no código). Feature lineage por feature:
`raw columns → transformation → feature`.

## Esquema del dataset modelable

Qué columnas formarían el dataset final (entity ID, fecha, target y features
seleccionadas para la primera iteración).

## Plan de verificación

Cómo verificar cada feature una vez construida: cálculo, ventanas, missing,
estabilidad temporal, ausencia de leakage, reproducibilidad.

## Riesgos, descartes y preguntas abiertas

- Familias o features rechazadas con su motivo.
- Información de negocio pendiente de confirmar con el usuario o un experto.
- **Siguiente paso recomendado**: qué conjunto de features (normalmente las P0)
  conviene probar primero contra el baseline.

> Nota de desviación respecto a `templates/SKILL.md`: la plantilla define la sección
> Output como `Resumen / Hallazgos / Evidencia / Recomendaciones`. Esta skill produce
> un **plan de diseño**, no una auditoría de hallazgos, por lo que sustituye
> "Hallazgos" por secciones de diseño (feature strategy, feature inventory, contrato
> temporal, priorización, leakage notes, plan de implementación, esquema del dataset
> modelable, plan de verificación) y agrupa riesgos, descartes y preguntas abiertas.
> El candidate exige que cada feature esté atada a una hipótesis, una ventana y una
> justificación de viabilidad, y que el output esté priorizado. Además, la skill
> **escribe un artefacto en disco** (`reports/features/…`), algo que la plantilla no
> contempla, para dar persistencia y trazabilidad al plan.

# Verificación final

Antes de terminar comprobar:

- [ ] Se completaron todos los pasos del workflow.
- [ ] Todas las familias de features se consideraron y las no aplicables se
      descartaron con motivo explícito.
- [ ] Cada feature propuesta tiene hipótesis, inputs, ventana, viabilidad en
      inferencia, riesgo de leakage, prioridad y coste.
- [ ] Se construyó el contrato temporal (inputs válidos vs inválidos respecto al
      prediction timestamp).
- [ ] Se ejecutaron los checks deterministas disponibles y su resultado consta en el
      reporte.
- [ ] Se revisaron los falsos positivos: sin features sin hipótesis, sin familias sin
      soporte en los datos, sin transformaciones redundantes.
- [ ] Se evaluó la viabilidad en producción de cada feature.
- [ ] La información que falta está en "Preguntas abiertas", no inventada.
- [ ] No se escribió código de construcción de features.
- [ ] No se entrenó ningún modelo ni se hizo feature selection.
- [ ] El reporte se escribió en `reports/features/…md` (sin sobrescribir un archivo
      previo) y su ruta se comunicó al usuario.
- [ ] El archivo incluye el frontmatter de trazabilidad (skill, versión, fecha,
      inputs, estado).
- [ ] El archivo no contiene datos sensibles más allá de la evidencia mínima
      necesaria.

# Modos de fallo conocidos

## Fallo 1 — Feature explosion

Descripción: se generan decenas o cientos de variables sin priorización.

Causa: aplicar todas las transformaciones posibles a todas las columnas.

Mitigación: paso 3 y sección "Priorización"; toda feature lleva prioridad P0/P1/P2 y
el reporte destaca el conjunto mínimo a probar primero. Más features no implica mejor
modelo.

## Fallo 2 — Features sin hipótesis

Descripción: se proponen transformaciones arbitrarias sin una señal de negocio
esperada.

Causa: crear variables por costumbre técnica en lugar de por hipótesis.

Mitigación: regla de atar cada feature a una hipótesis; una feature sin hipótesis no
entra en el inventory.

## Fallo 3 — Temporal leakage en agregaciones

Descripción: rolling, tendencias, EWMA o acumulados incorporan información del
período actual o futuro.

Causa: la ventana de agregación no excluye `t` y `t+1`.

Mitigación: contrato temporal explícito y check determinista de fechas de la ventana
frente al prediction timestamp.

## Fallo 4 — Ventana temporal incorrecta

Descripción: una feature bien formulada se construye con una ventana que incluye
períodos inválidos (p. ej. `consumo_promedio_3m` que incluye el mes objetivo).

Causa: no se fija qué períodos son legítimos antes de definir la feature.

Mitigación: paso 1 y contrato temporal; cada feature declara su ventana y se comprueba
contra el prediction timestamp.

## Fallo 5 — Redundancia

Descripción: se proponen múltiples transformaciones casi idénticas de la misma señal.

Causa: no se compara entre features candidatas.

Mitigación: check determinista de correlación / near-duplication en el paso 4;
consolidar pares casi idénticos.

## Fallo 6 — Inventar familias sin soporte en los datos

Descripción: se proponen features geoespaciales sin coordenadas, de grafo sin
topología o temporales sin fechas.

Causa: se listan familias "conceptualmente útiles" sin comprobar la estructura real.

Mitigación: paso 2 y checks de soporte de estructura; una familia sin evidencia en
los datos se descarta con motivo.

## Fallo 7 — Features inviables en producción

Descripción: una feature usa información que solo existe en el análisis offline.

Causa: no se comprueba qué información existe en el momento real de scoring.

Mitigación: check de viabilidad en producción; esas features se marcan Inválida o
Válida con condiciones y no entran en P0.

## Fallo 8 — No respetar los límites de la validación

Descripción: una fórmula correcta contamina la validación porque se calcula sobre
todo el dataset antes del split (target encoding, normalizaciones, agregaciones
globales).

Causa: se diseña la feature sin considerar la estrategia de validación.

Mitigación: sección "Leakage notes" y regla explícita; el plan indica qué debe
ajustarse solo dentro de la ventana o fold correspondiente.

## Fallo 9 — Confundir feature generation con feature selection

Descripción: el reporte decide qué variables conservar a partir de importancia o
métricas.

Causa: se solapan dos problemas relacionados pero distintos.

Mitigación: sección "Cuándo NO usar" y reglas; la skill diseña y prioriza por
hipótesis y viabilidad, no selecciona por rendimiento observado.

## Fallo 10 — Sobreoptimizar para la hackathon

Descripción: el feature engineering se orienta a maximizar el score del concurso en
lugar de representar producción.

Causa: presión por el resultado inmediato.

Mitigación: regla explícita; el plan prioriza features reproducibles y viables en el
momento real de predicción.

## Fallo 11 — Sobrescribir un reporte anterior

Descripción: se guarda el nuevo reporte con el mismo nombre y se pierde el anterior.

Causa: no se comprueba la existencia del archivo antes de escribir.

Mitigación: paso 5 del workflow; ante colisión de fecha, añadir sufijo `-02`, `-03`,
… y no sobrescribir.

# Límites

Esta skill no garantiza:

- que las features propuestas mejoren el modelo sin probarlas contra el baseline;
- detectar leakage que solo es visible con conocimiento del proceso de negocio;
- la corrección semántica de las columnas cuando no hay data dictionary;
- la estabilidad de las features ante cambios de comportamiento futuros;
- que el coste de implementación estimado sea exacto;
- sustituir el criterio de un experto del dominio sobre las hipótesis de negocio y el
  momento de predicción;
- reproducibilidad exacta entre ejecuciones (el juicio semántico puede variar).

# Referencias

Consultar únicamente cuando sean necesarias:

- `AGENTS.md` → "# Checks deterministas" (prioridad de la evidencia determinista),
  "# Criterios de evaluación" (correctitud, cobertura, fundamentación, falsos
  positivos, accionabilidad), "# Idioma", "# Simplicidad".
- `candidates/2026-08-31-build-features.md` → candidate de origen: problema observado,
  familias de features, contrato temporal, los 10 casos de verificación previstos
  (incluidas las trampas: Caso 1 tabular simple sin lags, Caso 3 temporal leakage
  trap, Caso 6 no coordinates, Caso 10 negative feature test), riesgos y dimensiones
  de evaluación (relevance, validity, temporal correctness, leakage avoidance,
  coverage, production feasibility, redundancy, actionability, reproducibility).
- `experiments/skills/understand-dataset/SKILL.md` → skill hermana para la comprensión
  estructural inicial del dataset.
- `experiments/skills/detect-leakage/SKILL.md` → skill hermana para auditar el data
  leakage de un pipeline o un conjunto de features ya construidos; define la frontera
  de alcance con esta skill.
- `experiments/skills/design-validation/SKILL.md` → skill hermana que fija la
  estrategia de validación dentro de cuyos límites deben construirse las features.
