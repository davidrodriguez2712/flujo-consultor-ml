## Evidencia congelada, documentos vivos y aprobaciones

Antes de solicitar un gate o entregar un paquete, identificar qué versión concreta será revisada. Usar el nivel de detalle proporcional al encargo; estas pautas no obligan a crear todos los archivos del ejemplo.

| Clase | Ejemplos | Tratamiento |
|---|---|---|
| Documentos vivos | STATE, MANUAL, TASKS, planes de análisis y notas de trabajo. | Se actualizan durante el proyecto. Si sustentan una decisión, congelar una copia de la versión revisada. |
| Evidencia congelada | Inputs autorizados, contratos, código, outputs y copias de planes que sustentan un gate. | Conservar versión, ruta relativa y SHA-256 de cada archivo en un manifest del paquete. Verificar antes de revisar y antes de entregar. |
| Aprobaciones | Decisión humana, reviewer, fecha, alcance y límites de aceptación. | Registrar fuera del paquete congelado y vincular al manifest exacto mediante ruta, versión y SHA-256. |

Un hash de un archivo vivo identifica sus bytes en ese momento; no conserva su historial. Para conservar una versión, copiarla a una ruta histórica antes de calcular el hash. Excluir del paquete el estado canónico y las vistas que deben seguir actualizándose. No modificar los snapshots de capacidades ni los recursos propiedad de ACOS para gestionar evidencia del engagement.

### Procedimiento de freeze

1. Delimitar el paquete y enumerar sus archivos. Copiar los documentos vivos relevantes a rutas históricas dentro del proyecto autorizado; registrar también su ruta de origen. Reutilizar evidencia inmutable existente cuando corresponda, sin duplicar datos sensibles innecesariamente.
2. Registrar ID/versión del paquete, fecha, propósito y rutas relativas con SHA-256 de los archivos. Guardar el manifest fuera de su propia lista de archivos; calcular su hash después de cerrarlo.
3. Verificar todos los hashes. Registrar cualquier discrepancia como bloqueo para la revisión del paquete; no reemplazar el hash esperado para ocultarla.
4. Obtener revisión y aceptación humana del manifest exacto. La aprobación se guarda fuera del paquete para evitar que registrar la decisión altere la evidencia aprobada. En ACOS, referenciar ese registro y la evidencia en `gate_reviews` y DECISIONS antes de avanzar; conservar el esquema vigente del state.
5. Continuar actualizando los documentos vivos. Una corrección de evidencia requiere una nueva versión y revisión del alcance afectado: conservar el original, indicar paquete anterior, archivos cambiados, motivo e impacto sobre la aceptación previa. No transferir una aprobación automáticamente a la versión nueva.

Ejemplo de rutas para un gate de análisis:

```text
reports/analysis/
├── frozen-01/
│   └── analysis_plan.md       # copia histórica del plan vivo
├── evidence-manifest-01.yaml # rutas y hashes; no se incluye a sí mismo
├── approval-01.md            # referencia al hash del manifest aprobado
└── evidence-manifest-02.yaml # solo si existe una corrección documentada
analysis/analysis_plan.md     # plan vivo que puede evolucionar
```

El manifest de inicialización `.acos/manifest.yaml` identifica la composición inicial del workspace; no sustituye un manifest de evidencia de negocio. `acos validate` ejecuta sus checks existentes: estas pautas no añaden verificación automática de paquetes históricos ni aprueban gates por sí mismas. Usar el template de [`../templates/delivery-and-handoff.md`](../templates/delivery-and-handoff.md) para documentar el paquete y su aceptación.

## Reproducción del recorrido completo

Cuando una conclusión depende de cálculos, transformaciones o modelos, documentar el recorrido realmente ejecutado: inputs → transformaciones → persistencia → lectura → cálculo/fit → outputs. Una reproducción debe respetar las fronteras de serialización del pipeline original; usar directamente un objeto en memoria puede cambiar tipos o valores y, con ellos, los resultados.

Registrar lo pertinente al proyecto:

- fuentes/snapshots y hashes, código/configuración, comandos en orden y directorio de ejecución;
- versión del runtime, dependencias fijadas, plataforma y recursos que puedan afectar el resultado; seeds y fuentes de no determinismo conocidas;
- cada escritura y lectura material: ruta relativa, formato, writer/reader, opciones, esquema/tipos, precisión numérica, fechas/timezone, encoding, nulos, keys y orden si afecta al consumidor;
- qué artifact persistido consume cada paso, incluidas features y targets usados en fit; no sustituirlo por una reconstrucción en memoria sin verificar equivalencia;
- outputs esperados y criterios de comparación acordados antes del nuevo run.

No imponer CSV ni un formato universal. Para SQL o servicios, identificar query, snapshot/versionado, parámetros y reglas de lectura equivalentes. Un hash prueba identidad de bytes, no que dos pipelines ejecutaron el mismo recorrido o que dos artifacts diferentes sean semánticamente equivalentes.

### Comparar y resolver discrepancias

1. Reproducir en un destino nuevo autorizado, conservando el run original, sus outputs, manifest y decisiones. Resolver dependencias y documentar límites sin reabrir un holdout para seleccionar estrategias.
2. Comparar en cada frontera: esquema/tipos, keys únicas, filas/cobertura y orden material. Alinear por keys explícitas antes de comparar valores; no ocultar duplicados o pérdidas mediante un join.
3. Comparar outputs finales, métricas y decisiones. Definir qué debe ser exacto (por ejemplo, IDs seleccionados o regla de desempate) y qué admite tolerancia numérica, con unidades y motivo. Valores cercanos no garantizan el mismo ranking, threshold o split de un modelo.
4. Ante una discrepancia, registrar ambas ejecuciones, la primera frontera distinta y su impacto. Revisar entorno, parsing, serialización y método antes de atribuirla a ruido. Conservar el intento fallido y generar outputs nuevos para la corrección.
5. No ampliar tolerancias para convertir un fallo en PASS. Si el criterio debe cambiar por una razón justificada, registrar la decisión, su efecto y la revisión humana del alcance afectado. Declarar qué parte pudo reproducirse y qué sigue pendiente.

Usar el registro de reproducción en [`../templates/delivery-and-handoff.md`](../templates/delivery-and-handoff.md). El procedimiento es explícito: `acos validate` no ejecuta el análisis ni verifica por sí mismo su reproducibilidad.

## QA de cifras, etiquetas y períodos

Revisar la identidad de cada resultado material junto con su valor. Una cifra correcta atribuida a otro método, población o período puede cambiar la conclusión.

1. Identificar en el artifact fuente la métrica, método/comparador, población, unidad, denominador y período/cutoff correspondientes. Usar keys explícitas; si falta una key o hay varias filas candidatas, resolver la ambigüedad o declarar el bloqueo.
2. Definir períodos con inicio/fin, límites incluidos/excluidos y timezone cuando importen. Distinguir fecha de extracción, fecha de scoring, ventana de observación y ventana del outcome; no usarlas como fechas intercambiables.
3. Para “último”, “anterior” o “actual”, declarar la regla y fecha concreta. Filtrar el método/población pertinentes y los períodos elegibles y completos antes de ordenar por fecha/cutoff. El último período observado puede no ser el último período con outcomes maduros. Las keys y el valor citado deben mantenerse al reordenar filas.
4. Contrastar títulos, leyendas, texto, tablas y logs con las keys de la fuente y los valores con su regla de redondeo. Reconciliar numeradores/denominadores y unidades; no aceptar una etiqueta porque su cifra aparece en alguna fila.
5. Registrar discrepancias y su impacto sobre recomendaciones o gates. Conservar el original, emitir una corrección trazable y revisar la aceptación afectada según el procedimiento de freeze.

El checklist y el registro copiable están en [`../templates/findings-and-qa.md`](../templates/findings-and-qa.md). Estos checks requieren revisión explícita del artifact: `acos validate` no interpreta automáticamente títulos, leyendas ni períodos de los entregables.

