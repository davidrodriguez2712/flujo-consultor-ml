---
name: understand-dataset
description: >-
  Revisa uno o varios datasets nuevos ANTES del modelado y produce un reporte
  estructurado de comprensión: unidad de observación probable, claves e
  identificadores, granularidad y estructura temporal, cobertura temporal,
  target(s) candidato(s) y el momento en que se conoce su valor, calidad básica
  (duplicados exactos y lógicos, missing, constantes, cardinalidades), relaciones
  entre tablas y riesgos de leakage (target leakage, temporal leakage, variables
  post-evento). Separa siempre Hechos / Hipótesis / Preguntas abiertas y prioriza
  los hallazgos por severidad (crítico / alto / medio / informativo).
  NO hace EDA exhaustivo de distribuciones, NO hace feature engineering, NO entrena
  ni propone modelos y NO asume que el dataset está listo para modelar.
  Úsala al recibir datos o una estructura desconocida, una tabla o fuente nueva,
  una nueva versión del dataset o un proyecto heredado; no la uses para datasets
  pequeños ya documentados ni cuando el objetivo real es el análisis exploratorio
  de distribuciones.
status: experimental
version: 0.1.0
domain: data-science
---

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
- existe riesgo de variables generadas después del evento a predecir;
- se necesita revisar posibles problemas de leakage antes de empezar a modelar.

Ejemplos de disparador:

> Acabo de recibir estos archivos. Entiende primero la estructura antes de modelar.

> Analiza este dataset y dime qué representa una observación.

> Revisa estas tablas antes de que empiece el feature engineering.

> Identifica variables que no deberían utilizarse para predecir.

> Acabamos de recibir los datos de EQUANS. Primero necesitamos entenderlos.

# Cuándo NO usar

No utilizar esta skill cuando:

- el dataset es pequeño y ya está completamente documentado (data dictionary claro,
  unidad de observación y target conocidos): la revisión profunda añade coste sin
  valor suficiente;
- el objetivo real es un EDA de distribuciones, visualización o estadística
  descriptiva;
- ya existe una comprensión validada del dataset y solo se quiere feature
  engineering, selección de variables o modelado;
- la tarea pedida es entrenar, comparar o seleccionar modelos;
- no hay acceso a los datos ni a su estructura (ni columnas, ni tipos, ni muestra):
  no hay nada que inspeccionar.

# Inputs

## Obligatorios

- Al menos una de:
  - una o varias fuentes de datos inspeccionables (CSV, Parquet, Excel, JSON,
    DataFrame en memoria);
  - **o** la estructura de esas fuentes: nombres de columnas, tipos de datos y una
    muestra de registros.

## Opcionales

- Data dictionary o documentación del dataset.
- Definición del problema de negocio.
- Descripción del target y del momento de predicción (cuándo se hace la predicción y
  qué información existe en ese instante).
- Información sobre columnas de fecha y sobre identificadores.
- Relaciones conocidas entre tablas.
- Restricciones del proyecto, incluidas políticas de confidencialidad,
  almacenamiento y procesamiento (p. ej. las condiciones de datos de EQUANS).
- Ruta de salida del reporte: si se indica, se usa en lugar de la ruta por
  defecto (`reports/dataset/dataset-understanding-<YYYY-MM-DD>.md`).

Cuando falte contexto crítico, identificarlo como pregunta abierta en lugar de
inventarlo.

# Preconditions

Antes de ejecutar el workflow debe ser cierto:

- Se puede inspeccionar la estructura (columnas, tipos) y una muestra de cada tabla.
- Está permitido procesar los datos de acuerdo con las políticas del proyecto.
- Existe un objetivo de negocio, aunque sea provisional, o al menos una pregunta que
  el modelo pretende responder.

# Workflow

## 1. Comprender el problema

- Recoger lo declarado por el usuario: objetivo de negocio, target candidato, momento
  de predicción, restricciones.
- Anotar qué información de contexto falta (definición exacta del positivo, ventana de
  performance, significado de columnas ambiguas). No inventarla: pasa a "Preguntas
  abiertas".
- Fijar el alcance: qué tablas entran en la revisión.

## 2. Analizar los inputs

- Construir un inventario de tablas. Por cada tabla registrar: nombre, nº de filas,
  nº de columnas, tipos por columna y una muestra de registros.
- Leer el data dictionary y la documentación si existen; marcar qué columnas quedan
  sin describir.

## 3. Ejecutar el procedimiento

Recorrer el checklist por tabla y luego entre tablas. Para cada punto, apoyarse
primero en los checks deterministas y registrar la evidencia.

Por tabla:

- **Unidad de observación probable**: qué representa una fila. Aportar evidencia
  (unicidad de una combinación de columnas, patrón de repetición por entidad).
- **Claves e identificadores**: claves candidatas y business key; comprobar unicidad.
  Distinguir **duplicados exactos** (fila entera repetida) de **duplicados respecto a
  una clave de negocio** (misma entidad-periodo con valores distintos).
- **Granularidad**: nivel de detalle de una fila. Considerar explícitamente panel
  data (`entidad × periodo`), no solo `entidad`.
- **Estructura temporal**: columnas de fecha, orden temporal, cobertura (rango
  mínimo-máximo) y huecos.
- **Target(s)**: target(s) candidato(s), su distribución y balance, y —crítico— **en
  qué momento se conoce su valor** respecto al momento de predicción.
- **Calidad**: proporción de missing por columna; columnas constantes o
  casi-constantes; columnas de cardinalidad muy alta (posibles identificadores o
  texto libre).

Entre tablas:

- **Relaciones**: columnas compartidas, cardinalidad del join (1:1, 1:N, N:M) y
  riesgo de fan-out (un join que multiplica filas y altera la unidad de observación).

Riesgos metodológicos:

- **Candidatos a leakage**, cada uno **con justificación explícita**, no solo por el
  nombre de la columna:
  - target leakage: la variable deriva del target o lo contiene;
  - temporal leakage: la variable usa información posterior al momento de predicción;
  - variables post-evento: se generan después del evento a predecir (resultado de
    inspección, importe recuperado, consumo del mes siguiente).
- **Variables que requieren validación de negocio**: su significado o su momento de
  generación no puede determinarse solo con los datos.

## 4. Verificar el resultado

- Recorrer la checklist de "Verificación final".
- Comprobar que cada hallazgo crítico o alto tiene evidencia observable, o está
  marcado como `[Hipótesis]` o movido a "Preguntas abiertas".
- Revisar la tasa de falsos positivos: si se han marcado muchas columnas como
  sospechosas de leakage, revisar la justificación de cada una y descartar las
  débiles.

## 5. Construir el output

- Redactar el reporte con la estructura de la sección "Output".
- No transformar el reporte en una propuesta de modelo.
- **Persistir el reporte** como archivo `.md` en
  `reports/dataset/dataset-understanding-<YYYY-MM-DD>.md` (fecha real de
  ejecución; crear la carpeta `reports/dataset/` si no existe). No sobrescribir:
  si ya existe un archivo con esa fecha, añadir sufijo `-02`, `-03`, … Si el
  usuario indicó una ruta de salida, usar esa.
- Encabezar el archivo con el frontmatter de trazabilidad (ver "Output"):
  skill, versión, fecha real, proyecto si se conoce, inputs analizados —con
  `sha256` cuando sean archivos locales— y una línea de estado.
- Respetar las políticas de confidencialidad del proyecto: no volcar en el
  archivo datos sensibles, PII ni muestras de registros más allá de lo
  imprescindible como evidencia (relevante para EQUANS).
- Devolver al usuario un resumen breve **y la ruta del archivo escrito**.

# Checks deterministas

Siempre que sea posible, utilizar evidencia determinista antes de realizar
inferencias. Ejecutar estas comprobaciones ad hoc sobre los datos (p. ej. con
pandas); **no** crear scripts en `scripts/` para esto (ver `AGENTS.md` →
"# Simplicidad").

Checks disponibles:

- **Duplicados exactos**: `df.duplicated().sum()`.
- **Unicidad de clave candidata**: `df.groupby(keys).size().max()` (> 1 ⇒ la clave no
  es única; hay duplicados lógicos o la granularidad es más fina).
- **Constantes / cardinalidad**: `df.nunique()` por columna (1 ⇒ constante; ≈ nº de
  filas ⇒ identificador o texto libre).
- **Missing**: `df.isna().mean()` por columna.
- **Cobertura temporal**: `min` / `max` de las columnas de fecha, nº de periodos,
  detección de huecos; monotonía por entidad.
- **Relaciones entre tablas**: columnas compartidas; para una relación candidata,
  comprobar unicidad de la clave en cada lado para determinar la cardinalidad y el
  riesgo de fan-out.
- **Señal de leakage** (indicio, no prueba): correlación o AUC univariante de una
  variable sospechosa frente al target; un valor casi perfecto refuerza la sospecha
  pero no la confirma por sí solo.

# Reglas

La skill debe:

- separar explícitamente Hechos, Hipótesis y Preguntas abiertas;
- justificar por qué una variable es sospechosa de leakage (mecanismo concreto), no
  solo señalarla;
- priorizar los hallazgos por severidad (crítico / alto / medio / informativo);
- declarar el target como hipótesis cuando no exista evidencia suficiente para
  confirmarlo;
- preferir los checks deterministas antes que las inferencias basadas en el nombre de
  una columna;
- señalar como pregunta abierta la información que falta para continuar (p. ej. para
  diseñar la validación).

La skill no debe:

- convertir una hipótesis en un hecho;
- asumir la semántica de una columna únicamente por su nombre;
- marcar como leakage toda variable muy predictiva sin justificar el mecanismo;
- entrenar modelos ni proponer un modelo, algoritmo o conjunto de hiperparámetros;
- realizar un EDA exhaustivo de distribuciones y perder el foco metodológico;
- asumir que el dataset está listo para modelar;
- ignorar las políticas de confidencialidad, almacenamiento o procesamiento del
  proyecto.

# Output

El reporte se entrega en dos formas: (a) un resumen en la respuesta al usuario;
(b) un archivo `.md` persistido en
`reports/dataset/dataset-understanding-<YYYY-MM-DD>.md` (o la ruta indicada por
el usuario), encabezado con el frontmatter de trazabilidad. El archivo es la
fuente de trazabilidad; su contenido bajo el frontmatter usa la estructura de
esta sección.

Frontmatter de trazabilidad del archivo:

```yaml
---
skill: understand-dataset
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

- Qué datasets/tablas hay.
- Unidad de observación probable de cada tabla.
- Target candidato y momento en que se conoce su valor.
- ¿Parece posible definir una estrategia de validación con la información disponible?

## Hallazgos

Agrupados por severidad: **Crítico**, **Alto**, **Medio**, **Informativo**.

Cada hallazgo se etiqueta como `[Hecho]` (verificable directamente en los datos) o
`[Hipótesis]` (interpretación razonable no confirmable solo con los datos), e incluye
una referencia a la evidencia que lo respalda.

## Evidencia

Resultado de los checks deterministas que respaldan los hallazgos (conteos,
unicidad de claves, missing, cobertura temporal, cardinalidad de joins, señales de
leakage).

## Preguntas abiertas

Información que requiere confirmación del usuario o de un experto de negocio antes de
continuar con el análisis (definición del positivo, momento de generación de
variables ambiguas, ventana de observación, relaciones entre tablas no verificables).

## Recomendaciones

Qué investigar o resolver antes de modelar. No es una propuesta de modelo.

> Nota de desviación respecto a `templates/SKILL.md`: la plantilla define la sección
> Output como `Resumen / Hallazgos / Evidencia / Recomendaciones`. Esta skill añade
> las subsecciones "Hallazgos" por severidad (con etiqueta `[Hecho]` / `[Hipótesis]`)
> y "Preguntas abiertas" porque el candidate exige priorización explícita de riesgos
> y separación entre hechos, hipótesis e información pendiente de confirmar. Además,
> la skill **escribe un artefacto en disco** (`reports/dataset/…`), algo que la
> plantilla no contempla, para dar persistencia y trazabilidad a la revisión.

# Verificación final

Antes de terminar comprobar:

- [ ] Se completaron todos los pasos del workflow.
- [ ] La unidad de observación de cada tabla está identificada o marcada como
      `[Hipótesis]`.
- [ ] La estructura temporal (fechas, orden, cobertura, huecos) fue analizada cuando
      existe información temporal.
- [ ] Cada hallazgo crítico o alto tiene evidencia observable, o está etiquetado como
      `[Hipótesis]` o movido a "Preguntas abiertas".
- [ ] Cada variable señalada como sospechosa de leakage tiene una justificación de
      mecanismo.
- [ ] No se afirma cuál es el target sin evidencia suficiente.
- [ ] Los hechos están separados de las inferencias y de las preguntas abiertas.
- [ ] El output cumple el formato definido y prioriza los hallazgos por severidad.
- [ ] No se entrenó ningún modelo ni se propuso una arquitectura de modelo.
- [ ] El reporte se escribió en `reports/dataset/…md` (sin sobrescribir un
      archivo previo) y su ruta se comunicó al usuario.
- [ ] El archivo incluye el frontmatter de trazabilidad (skill, versión, fecha,
      inputs, estado).
- [ ] El archivo no contiene datos sensibles más allá de la evidencia mínima
      necesaria.

# Modos de fallo conocidos

## Fallo 1 — Inferir incorrectamente la semántica de una columna

Descripción: se determina qué significa una columna basándose solo en su nombre
(`status` puede representar múltiples cosas).

Causa: ausencia de data dictionary y tendencia a completar el hueco con una
suposición.

Mitigación: describir el significado como `[Hipótesis]` y llevarlo a "Preguntas
abiertas"; no usarlo como hecho en el resto del reporte.

## Fallo 2 — Elegir incorrectamente el target

Descripción: se asume que una variable binaria es el target cuando en realidad
representa otro evento.

Causa: varias columnas binarias plausibles y falta de definición del positivo.

Mitigación: presentar los targets candidatos, marcar la elección como `[Hipótesis]` y
pedir confirmación cuando no haya evidencia suficiente.

## Fallo 3 — Confundir capacidad predictiva con leakage

Descripción: se marca como leakage cualquier variable muy correlacionada con el
target.

Causa: se usa la correlación alta como prueba en lugar de como indicio.

Mitigación: exigir una justificación de mecanismo (cómo la variable incorpora
información del target o posterior al evento); si no existe, degradar la severidad y
moverlo a "Preguntas abiertas".

## Fallo 4 — No detectar leakage semántico

Descripción: una variable sin nombre evidente se generó después del evento y no se
detecta.

Causa: sin documentación de negocio, el momento de generación puede ser
indeterminable con los datos.

Mitigación: listar explícitamente las variables cuyo momento de generación no puede
verificarse como "requieren validación de negocio".

## Fallo 5 — Exceso de falsos positivos

Descripción: se marcan demasiadas columnas como potencialmente peligrosas y el
reporte pierde utilidad.

Causa: criterio de sospecha demasiado laxo.

Mitigación: paso 4 del workflow; revisar la justificación de cada sospechoso y
descartar los débiles antes de emitir el reporte.

## Fallo 6 — Convertirse en un EDA genérico

Descripción: el reporte se llena de estadísticas y gráficos de distribuciones y
pierde el foco estructural y metodológico.

Causa: arrastre del hábito de EDA.

Mitigación: la sección "Cuándo NO usar" y el objetivo declarado; el output no
contiene análisis de distribuciones salvo el balance del target.

## Fallo 7 — Sobreanalizar datasets simples

Descripción: se ejecuta una revisión profunda sobre un dataset pequeño y bien
documentado, con coste y tokens sin valor proporcional.

Causa: aplicar el workflow completo por defecto.

Mitigación: la sección "Cuándo NO usar"; ante un dataset ya documentado, confirmar la
estructura conocida de forma breve y detenerse.

## Fallo 8 — Sobrescribir un reporte anterior

Descripción: se guarda el nuevo reporte con el mismo nombre y se pierde el
anterior.

Causa: no se comprueba la existencia del archivo antes de escribir.

Mitigación: paso 5 del workflow; ante colisión de fecha, añadir sufijo `-02`,
`-03`, … y no sobrescribir.

# Límites

Esta skill no garantiza:

- detectar leakage que solo es visible con conocimiento del proceso de negocio;
- que el target identificado sea el correcto sin confirmación humana;
- la corrección semántica de las columnas cuando no hay data dictionary;
- que el dataset sea representativo del problema real o del proceso operativo;
- sustituir la validación con un experto del dominio;
- reproducibilidad exacta entre ejecuciones (el juicio semántico puede variar).

# Referencias

Consultar únicamente cuando sean necesarias:

- `AGENTS.md` → "# Checks deterministas" (prioridad de la evidencia determinista),
  "# Criterios de evaluación" (correctitud, cobertura, fundamentación, falsos
  positivos, accionabilidad), "# Idioma", "# Simplicidad".
- `candidates/2026-08-31-understand-dataset.md` → candidate de origen: problema
  observado, capacidad propuesta, riesgos y plan de verificación.
