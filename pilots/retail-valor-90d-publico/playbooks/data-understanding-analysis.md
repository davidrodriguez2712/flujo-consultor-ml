# Comprensión de datos y análisis

Usar esta ruta para saber qué representa una fuente, comprobar si permite responder una pregunta y producir análisis descriptivo/diagnóstico reproducible. El flujo de proyecto está en [`../workflow/project-lifecycle.md`](../workflow/project-lifecycle.md); acceso y persistencia están en [`../workflow/isolation-and-context.md`](../workflow/isolation-and-context.md).

## Cuándo usar

- aparece una fuente, tabla, extract o feed que aún no se comprende;
- la pregunta requiere SQL, conteos, cohortes, EDA o explicación de una variación;
- se necesita auditar calidad o verificar que una métrica se calcula sobre la población correcta;
- hay que determinar si los datos alcanzan antes de decidir experimento o modelo.

No es necesario crear un modelo para completar un análisis. Si se busca estimar el efecto de una intervención o seleccionar casos futuros, pasar al playbook de [`experimentos y modelos`](experiments-and-models.md).

## 1. Comprender la fuente

Antes de agregar o cruzar datos, establecer lo que se sabe:

| Aspecto | Preguntas |
|---|---|
| Fuente y lineage | ¿Quién la produce? ¿Qué proceso genera filas y cómo llega al snapshot usado? |
| Grain | ¿Qué representa una fila: transacción, tarjeta, cliente-mes, evento u otra unidad? |
| Keys y entidades | ¿Qué keys identifican fila/entidad? ¿Son únicas? ¿Pueden faltar o reutilizarse? |
| Tiempo | ¿Qué timestamps existen, zona horaria, frecuencia, fecha de extracción y atraso de datos? |
| Semántica | ¿Qué significan estado, monto, target, cancelación, conversión u otras columnas? ¿Quién lo confirma? |
| Cobertura | ¿Qué poblaciones, canales y períodos están incluidos o excluidos? |
| Disponibilidad | ¿Qué información existía al momento de la decisión y qué llega después? |
| Uso permitido | ¿Qué clasificación, permisos, retención y destinos aplican? |

Registrar definiciones en `DATA_CONTRACT.md` o equivalente cuando deban persistir. No inferir semántica por el nombre de una columna ni dar por confirmada una hipótesis del consultor.

## 2. Auditar calidad antes de interpretar

Elegir checks vinculados al uso; no producir un inventario de anomalías sin impacto. Considerar:

- completitud y patrones de missingness;
- unicidad y duplicados en la key/grain esperado;
- integridad referencial y cardinalidad de joins;
- rangos, tipos, unidades, valores imposibles y cambios de definición;
- cobertura por período, entidad, canal y segmento;
- frescura, atraso y ventanas de observación incompletas;
- reconciliación con totales o fuentes independientes cuando exista un referente.

Por hallazgo registrar: evidencia, período/población afectada, severidad, efecto potencial en la pregunta y responsable/acción si se conoce. Distinguir error que invalida una conclusión, limitación que acota el uso y anomalía informativa.

Si un cambio de calidad puede explicar el cambio de negocio, separar primero cambio de proceso de datos de cambio real. Si no puede resolverse, limitar la conclusión o detener el análisis.

## 3. SQL y agregaciones

Antes de escribir la query, anotar:

1. pregunta y decisión;
2. población elegible y exclusions;
3. unidad/grain de salida;
4. keys y cardinalidad esperada por join;
5. numerador, denominador, período y maduración;
6. checks que detectarían duplicación o pérdida de filas.

Reglas de trabajo:

- agregar cada fuente al grain adecuado antes de unir fuentes de distinto grain;
- cuantificar filas y entidades antes/después de joins importantes;
- declarar filtros, ventanas, timezone y manejo de late data;
- presentar conteos junto a tasas y definir denominadores;
- conservar una query reproducible con fuente/snapshot y parámetros permitidos;
- comparar totals y cortes antes de explicar diferencias;
- evitar SQL dinámico o escritura a la base cuando el alcance solo autoriza lectura.

Ejemplo de una métrica de activación por cohorte: definir si la unidad es tarjeta o persona, la fecha de emisión, la regla de actividad y la ventana; incluir solo cohortes con la ventana completa o marcar maduración parcial. La definición debe confirmarla el owner del KPI.

## 4. EDA y análisis diagnóstico

Empezar con una pregunta o hipótesis concreta y estructurar los cortes:

- distribución y cobertura general;
- cambio temporal y eventos operativos relevantes;
- segmentos vinculados a una acción posible;
- composición/mix frente a desempeño dentro de segmentos;
- incertidumbre/tamaño de muestra cuando importe para decidir.

Separar el efecto de cambio en mix de una variación dentro de los grupos. No llamar causa a una diferencia observacional; evitar búsquedas indiscriminadas de segmentos y presentar como confirmatorios cortes exploratorios. Registrar hipótesis nuevas para análisis posterior.

Para tasas, incluir numerador y denominador. Para ventanas temporales, excluir o marcar observaciones que no hayan tenido tiempo de completar el outcome. Para segmentos pequeños, declarar fragilidad y evitar rankings que exageren ruido.

## 5. Hallazgos

Cada finding debe incluir:

- **Observación:** qué cambió o qué patrón se ve.
- **Población/período:** a quién y cuándo aplica.
- **Evidencia:** consulta, conteos, métrica, tabla o artifact reproducible.
- **Interpretación:** inferencia con mecanismo plausible, separada del hecho observado.
- **Confianza/límite:** qué puede y qué no puede concluirse.
- **Acción:** qué análisis, validación o decisión se recomienda.

Usar `../templates/findings-and-qa.md` (referencia no seleccionada: `../templates/findings-and-qa.md`) si el resultado se va a revisar o entregar. No presentar causalidad, impacto o predicción a partir de un corte descriptivo.

## Salida y condiciones de cierre

Entregar solo artifacts necesarios: contrato de datos, query, auditoría/findings y revisión según alcance. La ruta termina cuando la pregunta está respondida con evidencia suficiente, el resultado se acota por una limitación, o se documenta que los datos no permiten responder. Registrar fuentes, grain, filtros, denominadores y condiciones de reproducción.
