# Evaluación exploratoria — contrato temporal, ronda 02

Fecha local: 2026-10-07 (America/Lima). Timestamps UTC: 2026-10-08. Status: ejecución, checks y review por agentes completados; review humana externa pendiente.

## Pregunta y comparación

¿El contrato temporal reduce errores frente a pautas actuales, sin excluir válidos ni inventar disponibilidad? Diseño aprobado; seis cases nuevos de suscripciones/crédito sintético, doce filas, dos repeticiones por condición: 24 llamadas. Baseline=contenido actual de design-validation 0.1.0; treatment=mismo contenido más contrato temporal local 0.1.0. Comparación documental, no invocación nativa de skill ni modelo de negocio entrenado.

Task/inputs/schema comunes, contextos separados, orden alternado e invertido en repetición 2. Oracle y checker congelados antes de observar outputs. Revisores previos detectaron defectos de schema y runner: corregidos y probados antes del freeze. [Protocolo](protocol.md), [review previa](preregister-review.md), [rúbrica](semantic-rubric.md).

## Resultados deterministas

| Check | Baseline | Treatment |
|---|---:|---:|
| Calls sin error de runtime | 12/12 | 12/12 |
| JSON puro estricto | 8/12 | 9/12 |
| Outputs con contenido estructurado evaluable | 11/12 | 12/12 |
| Campos correctos / campos requeridos | 66/72 | 72/72 |
| Elegibilidad correcta / filas requeridas | 22/24 | 24/24 |
| Gate comprobable NEEDS_REVIEW | 11/12 | 12/12 |

[Resultados reproducibles](deterministic-checks.json); cada run conserva checks y comando exacto del checker congelado.

La diferencia 66/72 frente a 72/72 proviene ENTERAMENTE de un output baseline malformado, E repetición 1. Falta el valor de label_availability_at_training para E1; el JSON no se puede parsear. Las dos filas permanecen en denominador como no evaluables, no como dos decisiones temporales incorrectas. No se reparó el texto ni se completaron campos desde reason.

Entre las filas estructuradas evaluables: baseline 22/22 elegibilidades y 66/66 campos; treatment 24/24 y 72/72. No hay admisiones indebidas, exclusiones ni indeterminaciones de válidos detectadas en esas filas. Para baseline, no extender esa conclusión a las dos no evaluables. Los gates visibles en el texto malformado no otorgan PASS del check estructurado.

## Casos y repetición

A separa extracción posterior y entrenamiento histórico; B prueba igualdad y +1 segundo; C feature futura y disponibilidad desconocida; D positivo temprano certificado y provisional; E cero provisional y certificación desconocida; F fila válida y offsets equivalentes.

Las clases estructuradas de ambas repeticiones coinciden con expected, excepto el output no evaluable E baseline1. Su repetición 2 es JSON evaluable y acierta. El defecto no se repite; no atribuir una frecuencia estable al suplemento. El baseline ya llega al techo de correctitud temporal en todas sus respuestas evaluables.

## Review semántica independiente

Dos revisores nuevos, separados del autor: [A/B/C](review-abc.md) y [D/E/F](review-def.md). Leyeron criterios y expected antes de outputs, sin recibir tally del autor; no modificaron evidencia. Son agentes, no revisores humanos externos. El coordinador contrastó citas y consolidó sus devoluciones.

Ninguno identificó razones temporales falsas ni intervalos inventados. E baseline1 tiene texto legible correcto, pero congruencia estructurada UNCLEAR por la omisión; no se cuenta como acierto de campo.

| Defecto semántico | Baseline | Treatment |
|---|---:|---:|
| Outputs con preguntas redundantes/problemáticas | 6 | 0 |
| Afirmaciones erróneas dentro de preguntas | 2 | 0 |
| Pregunta de pertinencia incierta | 0 | 1 |
| Fallos de autoridad textual | 0 | 0 |

En baseline, A/2, B/2, C/1, E/1, E/2 y F/2 (case/repetición) reabren instantes ya fijados. E2 añade el supuesto de que una extracción posterior impide auditar disponibilidad histórica; F2 dice anterioridad donde F1 tiene igualdad. Sus razones y decisiones evaluables siguen correctas. Treatment E2 incluye una hipótesis alternativa innecesaria para resolver E1; el reviewer la conserva como UNCLEAR conforme a la rúbrica, no como fallo inventado.

## Eficiencia observada

| Magnitud acumulada, doce calls | Baseline | Treatment |
|---|---:|---:|
| Tiempo de pared | 109,811 s | 113,289 s |
| Duración del proveedor | 97,342 s | 100,798 s |
| Coste reportado | USD 0,737532 | USD 0,825128 |

Total reportado: USD 1,562660. Coste y tokens son observaciones del CLI, no precios estimados. Treatment añade contenido y resultó más costoso en esta ronda. No inferir ahorro o velocidad general; servicio/cache/longitud de respuestas pueden influir.

## Integridad y límites

41 archivos congelados con hashes intactos; 24 sesiones distintas y modelo resuelto claude-sonnet-5-5. CLI 2.1.293, Python 3.13.2, macOS ARM64. Timestamps locales registrados antes de calls; precedencia sin anclaje externo. Pautas actuales copiadas byte a byte del Foundry; contrato copiado de docs ACOS. No se alteraron las rondas anteriores, el piloto cerrado o el Foundry.

Por call: argv, system prompt, cwd vacío, payload y hash, stdout/raw/result, stderr, metadata, tiempos, coste y checks. Flags solicitados: effort medium, safe-mode, sin herramientas/MCP/persistencia. Modelo efectivo visible; otros parámetros no acreditados independientemente por runtime y declarados unknown. No hubo reanudación ni selección favorable de resultados. Verificación de todos los artefactos al reanudar permanece como mejora opcional del runner local.

Task fija ejes y reglas explícitos; sigue siendo una auditoría guiada, no discovery. Dos repeticiones y dos industrias ficticias no demuestran generalidad ni significancia. No se incorpora el contrato al compiler por esta prueba.

## Interpretación y recomendación

Hay señales exploratorias de mejor entrega estructurada y menos preguntas redundantes en treatment. No hay ventaja demostrada en decisiones temporales entre outputs evaluables. El criterio prospectivo no debe transformarse en victoria de razonamiento por los seis campos no evaluables de baseline: el origen observado es serialización/omisión. Los fallos de formato y lectura se informan separados, tal como exigía el protocolo.

Conservar el contrato como propuesta documental local; no presentarlo como eficacia temporal probada, crear una skill duplicada o promover Foundry. Si se desea otra ronda, aislar cumplimiento de schema con un mecanismo común de salida estructurada y ampliar casos/repeticiones antes de atribuir una mejora. Esa continuación no está ejecutada ni implica modificar los expected de esta ronda.
