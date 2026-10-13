---
name: detect-leakage
description: >-
  Audita un dataset, un conjunto de features, un pipeline de preprocessing, una
  estrategia de validación o el código de feature engineering para detectar data
  leakage: información futura, posterior al evento objetivo o perteneciente al
  conjunto de evaluación que influye directa o indirectamente sobre el
  entrenamiento. Revisa familias de leakage: target leakage, post-event leakage,
  temporal leakage, train-test contamination, preprocessing leakage, target
  encoding leakage, aggregation leakage, join leakage, entity leakage, resampling
  leakage y cross-validation leakage. No analiza sólo los nombres de las columnas
  finales: revisa cómo se construyeron, qué timestamps usaron, qué tablas
  participaron, cuándo se ajustaron las transformaciones y cómo se hizo el split.
  Separa siempre Confirmado / Probable / Riesgo / No determinable y prioriza los
  hallazgos por severidad (crítico / alto / medio / bajo / informativo).
  NO elimina variables automáticamente, NO inventa timestamps ni semántica de
  negocio, NO marca como leakage toda variable muy predictiva y NO sustituye la
  validación de un experto del dominio.
  Úsala al recibir un dataset con target definido, al construir features
  temporales (lag, rolling, agregaciones), target encoding, feature selection,
  pipelines, cross-validation o joins nuevos, cuando un modelo obtiene métricas
  inesperadamente altas, o para auditar un modelo previo antes de validación real
  o producción; no la uses para la comprensión estructural inicial de un dataset
  (usa `understand-dataset`), para problemas sin target ni horizonte temporal, ni
  cuando la tarea es entrenar u optimizar un modelo.
status: experimental
version: 0.1.0
domain: data-science
---

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
- se realizan agregaciones o se incorporan tablas nuevas mediante joins;
- se utiliza target encoding, mean encoding u otra codificación basada en el
  target;
- se ejecuta feature selection o hyperparameter tuning;
- se construye un pipeline de preprocessing (imputación, scaling, encoding, PCA,
  resampling);
- se diseña o revisa una estrategia de validación (train/test split, split
  temporal, cross-validation, group split);
- un modelo obtiene métricas inesperadamente altas;
- una feature presenta una capacidad predictiva sospechosamente elevada
  (p. ej. AUC univariante ≈ 0.99);
- se prepara un modelo para validación real o producción;
- se desea auditar un modelo construido previamente.

Ejemplos de disparador:

> Revisa si estas features tienen leakage.

> Audita este pipeline antes de entrenar.

> Esta variable tiene un AUC univariado de 0.99. Investiga si puede existir
> leakage.

> Revisa si mis rolling features utilizan solamente información pasada.

> Revisa este split temporal.

> Identifica variables que no existirían en scoring.

> Acabamos de recibir los datos de EQUANS. Antes de modelar, identifica posibles
> fuentes de leakage.

# Cuándo NO usar

No utilizar esta skill cuando:

- lo que se necesita es la **comprensión estructural inicial** de un dataset
  desconocido (unidad de observación, claves, granularidad, target candidato,
  calidad básica): usar `understand-dataset`, que ya señala riesgos de leakage
  superficiales como parte de esa revisión;
- no hay acceso a **nada auditable**: ni a los datos ni a su estructura, ni a la
  lista/descripción de features, ni al código del pipeline, ni a una descripción
  de la estrategia de validación;
- el problema no es supervisado, o no existe target ni horizonte temporal
  respecto al cual razonar sobre "información futura";
- la tarea pedida es entrenar, comparar, seleccionar u optimizar un modelo;
- el dataset es pequeño, ya está completamente documentado y el pipeline es
  trivial (una sola tabla, sin features temporales, sin transformaciones
  ajustadas, split aleatorio simple justificado): la auditoría profunda añade
  coste sin valor suficiente.

# Inputs

## Obligatorios

- Al menos uno de:
  - una o varias fuentes de datos inspeccionables (CSV, Parquet, Excel, JSON,
    DataFrame en memoria);
  - la lista de features con su descripción o un data dictionary;
  - el código de feature engineering, joins, agregaciones o el pipeline
    (funciones, pipelines de sklearn, notebooks, scripts de preparación);
  - una descripción de la estrategia de validación (tipo de split, folds, orden
    temporal, grupos).

## Opcionales

- Definición del problema: target, evento objetivo, unidad de observación,
  entidad.
- **Prediction timestamp**: en qué momento se realiza la predicción y qué
  información existe en ese instante.
- Ventanas: observation window, prediction horizon, performance window.
- Fechas relevantes: fecha de observación, fecha del evento, fecha de inspección,
  fecha de generación de variables, fecha de corte, períodos de train y
  validación.
- Relaciones conocidas entre tablas.
- Métricas observadas del modelo y feature importance / AUC univariante.
- Restricciones del proyecto (políticas de confidencialidad, almacenamiento y
  procesamiento; p. ej. las condiciones de datos de EQUANS).
- Ruta de salida del reporte: si se indica, se usa en lugar de la ruta por
  defecto (`reports/leakage/leakage-audit-<YYYY-MM-DD>.md`).

Cuando falte contexto temporal o de negocio crítico, marcar el hallazgo
correspondiente como **No determinable** y llevarlo a "Preguntas abiertas". No
inventar timestamps ni semántica.

# Preconditions

Antes de ejecutar el workflow debe ser cierto:

- Existe un target o evento objetivo, aunque sea provisional.
- Hay al menos un artefacto auditable: datos, features descritas, o código del
  pipeline / validación.
- Está permitido procesar los datos de acuerdo con las políticas del proyecto.

# Workflow

## 1. Comprender el problema

- Fijar: target / evento objetivo, unidad de observación y entidad.
- Fijar el **prediction timestamp**: el instante en que el sistema debe decidir,
  y qué información conoce en ese instante. Para EQUANS: el momento de priorizar
  qué suministro inspeccionar, antes de la inspección.
- Situar el evento objetivo en la línea temporal del proceso de negocio
  (para EQUANS: detección → priorización → inspección → confirmación →
  recuperación → regularización).
- Anotar el contexto que falta (definición del positivo, ventanas, momento de
  generación de columnas ambiguas). No inventarlo: pasa a "Preguntas abiertas".
- Fijar el alcance: qué artefactos entran en la auditoría (features, pipeline,
  validación, código, tablas).

## 2. Analizar los inputs

- Inventariar lo disponible: lista de features, transformaciones, tablas y
  joins, pasos del pipeline, esquema de validación, fragmentos de código.
- Por cada elemento registrar qué se puede inspeccionar y qué no.
- Leer el data dictionary y la documentación si existen; marcar las columnas y
  transformaciones sin describir.

## 3. Ejecutar el procedimiento

Recorrer las familias de leakage como checklist. Para cada sospecha, apoyarse
primero en los checks deterministas y registrar **el mecanismo concreto** por el
que entraría información ilegítima (no basta el nombre de la columna).

**Sobre las columnas / features**

- **Target leakage**: la feature deriva del target, lo contiene o es una
  transformación casi directa de él.
- **Post-event leakage**: la variable sólo se genera después de conocerse el
  evento objetivo (resultado de inspección, energía recuperada, irregularidad
  confirmada, fecha de regularización, acciones posteriores a la inspección).
  Comparar su momento de generación con el prediction timestamp.
- **Temporal leakage**: features de lag, rolling o tendencia construidas sin el
  desplazamiento temporal correcto, o agregaciones que incorporan períodos
  posteriores al prediction timestamp.
- **Entity leakage**: información a nivel de entidad que en realidad resume
  observaciones futuras de esa misma entidad.

**Sobre el split y la validación**

- **Train-test contamination**: features globales calculadas antes de separar
  train y test; observaciones de la misma entidad repartidas entre train y test
  cuando deberían agruparse; split temporal con solape de fechas entre
  particiones.
- **Cross-validation leakage**: feature selection, tuning o encoding realizados
  usando el fold de validación; ausencia de `GroupKFold` cuando hay entidades
  repetidas; ausencia de `TimeSeriesSplit` / split temporal cuando hay orden
  temporal.

**Sobre el pipeline**

- **Preprocessing leakage**: `fit` / `fit_transform` sobre todo el dataset antes
  del split (SimpleImputer, StandardScaler, RobustScaler, PCA, selección de
  features, reducción de dimensionalidad). El problema está en el conjunto de
  observaciones usado para ajustar, no en la técnica.
- **Target encoding leakage**: encoding calculado con el target completo antes de
  la cross-validation o fuera de un pipeline que lo re-ajuste por fold.
- **Resampling leakage**: SMOTE u oversampling aplicado antes del split, de forma
  que observaciones sintéticas o duplicadas aparecen en train y test.
- **Aggregation / join leakage**: agregaciones calculadas fuera del período
  permitido; joins que incorporan columnas de una tabla generada después del
  evento objetivo.

Para cada hallazgo asignar un **nivel de confianza**:

- **Confirmado**: existe evidencia suficiente (código explícito, igualdad
  feature-target, solape de entidades verificado).
- **Probable**: señales fuertes pero falta una confirmación (nombre + AUC
  univariante casi perfecto + rol en el proceso de negocio).
- **Riesgo**: construcción metodológicamente peligrosa aunque no se observe el
  efecto todavía (p. ej. `fit_transform` antes del split sin medir el impacto).
- **No determinable**: la información disponible no permite concluir (depende del
  proceso de negocio o de un timestamp desconocido).

## 4. Verificar el resultado

- Recorrer la checklist de "Verificación final".
- Comprobar que cada hallazgo Crítico o Alto tiene un mecanismo explícito y
  evidencia, o está marcado como Riesgo / No determinable.
- **Revisar falsos positivos**: una feature puede tener gran poder predictivo y
  ser completamente válida (alta correlación con el target no demuestra
  leakage); un proxy fuerte del target no es necesariamente leakage; usar
  historia temporal pasada no es leakage temporal. Degradar o descartar las
  sospechas sin mecanismo.
- Si se han marcado demasiadas features como sospechosas, revisar una por una
  antes de emitir el reporte.

## 5. Construir el output

- Redactar el reporte con la estructura de la sección "Output".
- No transformar el reporte en una propuesta de modelo.
- Preferir recomendar la **reconstrucción correcta** (ventana temporal válida,
  transformación dentro del pipeline, split por grupos) antes que la eliminación
  de la variable, salvo que la variable sea intrínsecamente post-evento.
- **Persistir el reporte** como archivo `.md` en
  `reports/leakage/leakage-audit-<YYYY-MM-DD>.md` (fecha real de ejecución;
  crear la carpeta `reports/leakage/` si no existe). No sobrescribir: si ya
  existe un archivo con esa fecha, añadir sufijo `-02`, `-03`, … Si el usuario
  indicó una ruta de salida, usar esa.
- Encabezar el archivo con el frontmatter de trazabilidad (ver "Output"):
  skill, versión, fecha real, proyecto si se conoce, inputs auditados —con
  `sha256` cuando sean archivos locales— y una línea de estado.
- Respetar las políticas de confidencialidad del proyecto: no volcar en el
  archivo datos sensibles, PII ni muestras de registros más allá de lo
  imprescindible como evidencia (relevante para EQUANS).
- Devolver al usuario un resumen breve **y la ruta del archivo escrito**.

# Checks deterministas

Siempre que sea posible, utilizar evidencia determinista antes de realizar
inferencias. Ejecutar estas comprobaciones ad hoc (p. ej. con pandas /
scikit-learn o leyendo el código); **no** crear scripts en `scripts/` para esto
(ver `AGENTS.md` → "# Simplicidad").

Checks disponibles:

- **Relación feature-target casi determinista**: igualdad exacta, diferencia
  constante o mapeo 1:1 entre una feature y el target ⇒ target leakage
  confirmado.
- **Señal univariante** (indicio, no prueba): correlación o AUC univariante de
  una feature sospechosa frente al target; un valor casi perfecto refuerza la
  sospecha pero no la confirma.
- **Solape de entidades entre particiones**:
  `set(train[id]) & set(test[id])` no vacío ⇒ train-test contamination por
  entidad.
- **Solape temporal entre particiones**: `train[fecha].max()` ≥
  `test[fecha].min()` cuando el split pretende ser temporal.
- **Orden de operaciones en el código**: detectar `fit` / `fit_transform`,
  `SMOTE` / `resample`, target encoding o feature selection ejecutados **antes**
  del split, o fuera de un `Pipeline` incluido dentro de la cross-validation.
- **Ventana de agregación**: comprobar que las fechas usadas en una agregación /
  rolling son estrictamente anteriores al prediction timestamp de cada fila.
- **Timestamp de generación de una columna** (si se conoce) frente al prediction
  timestamp: fecha de generación posterior ⇒ post-event leakage.
- **Cardinalidad del join**: comprobar unicidad de la clave en cada lado para
  detectar fan-out y columnas traídas desde tablas posteriores al evento.

# Reglas

La skill debe:

- separar explícitamente **Confirmado / Probable / Riesgo / No determinable**;
- justificar el **mecanismo concreto** de cada sospecha (cómo entra información
  del target o posterior al evento), no sólo señalar la columna;
- priorizar los hallazgos por severidad (crítico / alto / medio / bajo /
  informativo);
- distinguir **dependencia temporal válida** (historia pasada) de **leakage
  temporal** (información futura);
- distinguir un **proxy fuerte** del target de un caso de leakage;
- auditar pipeline, cross-validation, resampling, splits y joins, no sólo los
  nombres de las columnas finales;
- declarar **No determinable** cuando falte el prediction timestamp, el target
  timestamp o el conocimiento del proceso de negocio;
- reconocer explícitamente el leakage semántico que sólo un experto de negocio
  puede confirmar.

La skill no debe:

- eliminar variables automáticamente;
- inventar timestamps o la semántica de una columna a partir de su nombre;
- marcar como leakage toda variable muy predictiva sin mecanismo;
- recomendar eliminar una variable cuando bastaría reconstruirla con una ventana
  temporal válida o mover una transformación dentro del pipeline;
- convertir una hipótesis en un hecho;
- entrenar modelos ni proponer un modelo, algoritmo o conjunto de
  hiperparámetros.

# Output

El reporte se entrega en dos formas: (a) un resumen en la respuesta al usuario;
(b) un archivo `.md` persistido en
`reports/leakage/leakage-audit-<YYYY-MM-DD>.md` (o la ruta indicada por el
usuario), encabezado con el frontmatter de trazabilidad. El archivo es la fuente
de trazabilidad; su contenido bajo el frontmatter usa la estructura de esta
sección.

Frontmatter de trazabilidad del archivo:

```yaml
---
skill: detect-leakage
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

- ¿Existe evidencia de leakage? ¿De qué tipo?
- Familias de leakage implicadas y componentes afectados (features, pipeline,
  validación, joins).
- ¿Parece posible definir / mantener una estrategia de validación fiable con la
  información disponible?

## Hallazgos

Agrupados por severidad: **Crítico**, **Alto**, **Medio**, **Bajo**,
**Informativo**.

Cada hallazgo incluye:

- componente afectado;
- familia de leakage;
- mecanismo / razón (cómo entra la información ilegítima);
- evidencia;
- nivel de confianza: **Confirmado / Probable / Riesgo / No determinable**;
- impacto potencial;
- prueba necesaria para confirmarlo;
- acción recomendada (preferir reconstrucción correcta antes que eliminación).

## Evidencia

Resultado de los checks deterministas que respaldan los hallazgos (relación
feature-target, señal univariante, solape de entidades o de fechas entre
particiones, orden de operaciones en el código, ventanas de agregación,
cardinalidad de joins).

## Preguntas abiertas

Información de negocio o de proceso necesaria para cerrar los hallazgos marcados
como **No determinable** (momento de generación de columnas ambiguas, prediction
timestamp exacto, ventanas de observación y performance, relaciones entre tablas
no verificables).

## Recomendaciones

Qué reconstruir, reordenar o verificar antes de confiar en las métricas del
modelo. No es una propuesta de modelo.

> Nota de desviación respecto a `templates/SKILL.md`: la plantilla define Output
> como `Resumen / Hallazgos / Evidencia / Recomendaciones`. Esta skill añade:
> subsecciones de "Hallazgos" por severidad; un nivel de confianza
> (Confirmado / Probable / Riesgo / No determinable) por hallazgo; y una sección
> "Preguntas abiertas". El candidate exige priorización explícita de riesgos y
> separación entre leakage confirmado, probable, riesgo metodológico e
> información pendiente de confirmar. Además, la skill **escribe un artefacto en
> disco** (`reports/leakage/…`), algo que la plantilla no contempla, para dar
> persistencia y trazabilidad a la auditoría.

# Verificación final

Antes de terminar comprobar:

- [ ] Se completaron todos los pasos del workflow.
- [ ] Se revisaron todas las familias de leakage aplicables (target, post-event,
      temporal, entity, train-test contamination, cross-validation,
      preprocessing, target encoding, resampling, aggregation, join).
- [ ] Cada hallazgo Crítico o Alto tiene un mecanismo explícito y evidencia, o
      está marcado como Riesgo / No determinable.
- [ ] Se ejecutaron los checks deterministas disponibles y su resultado consta en
      "Evidencia".
- [ ] Se revisó la tasa de falsos positivos: ninguna feature está marcada como
      leakage sólo por su alta correlación o poder predictivo.
- [ ] Se distinguió dependencia temporal válida de leakage temporal.
- [ ] La información que falta está en "Preguntas abiertas", no inventada.
- [ ] Ninguna recomendación elimina una variable cuando bastaría reconstruirla.
- [ ] No se entrenó ningún modelo ni se propuso una arquitectura de modelo.
- [ ] El output cumple el formato definido y prioriza los hallazgos por
      severidad.
- [ ] El reporte se escribió en `reports/leakage/…md` (sin sobrescribir un
      archivo previo) y su ruta se comunicó al usuario.
- [ ] El archivo incluye el frontmatter de trazabilidad (skill, versión, fecha,
      inputs, estado).
- [ ] El archivo no contiene datos sensibles más allá de la evidencia mínima
      necesaria.

# Modos de fallo conocidos

## Fallo 1 — Marcar cualquier variable predictiva como leakage

Descripción: se señala como leakage toda feature muy correlacionada con el
target.

Causa: se usa la correlación / el AUC univariante alto como prueba en lugar de
como indicio.

Mitigación: exigir un mecanismo concreto; si no existe, degradar la severidad a
Riesgo o No determinable y moverlo a "Preguntas abiertas".

## Fallo 2 — Inferir timestamps inexistentes

Descripción: se asume una fecha de generación o disponibilidad de una variable
que no consta en los datos.

Causa: el momento de disponibilidad depende del proceso de negocio y se completa
el hueco con una suposición.

Mitigación: marcar el hallazgo como No determinable y pedir el dato en
"Preguntas abiertas".

## Fallo 3 — Confundir proxy con leakage

Descripción: una variable es un proxy fuerte del target sin usar información
futura y se declara leakage.

Causa: no se distingue "predice muy bien" de "usa información que no existía".

Mitigación: comprobar si la variable estaba disponible antes del prediction
timestamp; si lo estaba, no es leakage (puede tener otros problemas).

## Fallo 4 — Exceso de falsos positivos

Descripción: se marcan demasiadas features como sospechosas y el reporte se
convierte en ruido.

Causa: criterio de sospecha demasiado laxo.

Mitigación: paso 4 del workflow; revisar el mecanismo de cada sospechoso y
descartar los débiles antes de emitir el reporte.

## Fallo 5 — No detectar leakage semántico

Descripción: una variable técnicamente legítima se genera en realidad después del
evento y no se detecta.

Causa: sin documentación de negocio, el momento de generación puede ser
indeterminable con los datos.

Mitigación: listar explícitamente las variables cuyo momento de generación no
puede verificarse como "requieren validación de negocio" en "Preguntas
abiertas".

## Fallo 6 — Analizar sólo nombres de columnas

Descripción: la auditoría se limita a la lista de features e ignora el
preprocessing, la cross-validation, el resampling, los splits y los joins.

Causa: arrastre de una revisión superficial tipo diccionario de datos.

Mitigación: el paso 3 obliga a recorrer las familias "sobre el split", "sobre el
pipeline" y los joins aunque no haya features sospechosas.

## Fallo 7 — Confundir dependencia temporal con leakage temporal

Descripción: se marca como leakage cualquier feature que use historia temporal.

Causa: no se diferencia información pasada válida de información futura inválida.

Mitigación: comprobar la ventana concreta: si todas las observaciones usadas son
anteriores al prediction timestamp, no hay leakage temporal.

## Fallo 8 — Recomendar eliminar en vez de reconstruir

Descripción: se propone descartar una variable cuando bastaría reconstruirla con
una ventana temporal válida o mover la transformación dentro del pipeline.

Causa: solución precipitada sin considerar la reconstrucción.

Mitigación: en "Recomendaciones", proponer primero la reconstrucción correcta;
reservar la eliminación para variables intrínsecamente post-evento.

## Fallo 9 — Sobrescribir un reporte anterior

Descripción: se guarda el nuevo reporte con el mismo nombre y se pierde el
anterior.

Causa: no se comprueba la existencia del archivo antes de escribir.

Mitigación: paso 5 del workflow; ante colisión de fecha, añadir sufijo `-02`,
`-03`, … y no sobrescribir.

# Límites

Esta skill no garantiza:

- detectar leakage que sólo es visible con conocimiento del proceso de negocio;
- que una feature declarada legítima lo sea, sin conocer su momento real de
  generación;
- sustituir la validación con un experto del dominio;
- detectar leakage cuando no hay acceso al código ni a la descripción del
  pipeline y la validación;
- reproducibilidad exacta entre ejecuciones (el juicio semántico puede variar).

# Referencias

Consultar únicamente cuando sean necesarias:

- `AGENTS.md` → "# Checks deterministas" (prioridad de la evidencia
  determinista), "# Criterios de evaluación" (correctitud, cobertura,
  fundamentación, falsos positivos, accionabilidad), "# Idioma", "# Simplicidad".
- `candidates/2026-08-01-detect-leakage.md` → candidate de origen: problema
  observado, familias de leakage, riesgos, y los 8 casos de verificación
  previstos (target leakage directo, post-event, temporal, preprocessing, target
  encoding, SMOTE antes del split, join, y el false positive challenge).
- `experiments/skills/understand-dataset/SKILL.md` → skill hermana para la
  comprensión estructural inicial; define la frontera de alcance con esta skill.
