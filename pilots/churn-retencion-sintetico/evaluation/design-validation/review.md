# Review exploratoria — design-validation 0.1.0

## Resultado

No hay evidencia suficiente de una mejora consistente frente al baseline. Ambos outputs cubren el problema y proponen acciones útiles; ambos contienen una explicación errónea del calendario. No se promueve ni modifica la skill ni se reabre un candidate.

Esta revisión la realiza el asistente que preparó el piloto: **no es review independiente**. Los criterios quedaron fijados antes de las ejecuciones y fuera de los directorios de los runners. No se alteraron expected ni las respuestas para corregir errores.

## Control de la comparación

- Dos sesiones nuevas de Claude Code; mismo modelo `claude-sonnet-5-5`.
- Mismo prompt, AGENTS y tres inputs; SHA-256 idénticos verificados.
- Baseline sin llamadas Skill; treatment invocó `design-validation` desde su bundle local 0.1.0.
- Ambos runners solo leyeron archivos dentro de sus directorios. Expected no fue leído.
- Los dos contextos permanecieron idénticos byte a byte al terminar; outputs conservados por el runner externo.
- Los inputs son contexto, diccionario y resultados deterministas resumidos; no se proporcionaron todas las filas CSV. Los runners no ejecutaron checks ni entrenamiento.

## Comparación con criterios fijados

| Criterio | Baseline | Treatment |
|---|---|---|
| Desarrollo temporal y test posterior aislado | Cubierto; propone 8 folds desde octubre de 2024, pero el mínimo de 8 meses de train es inconsistente | Cubierto; propone 9 folds desde septiembre y 6 meses mínimos, consistente |
| Disponibilidad de labels y pending | Regla exacta por label_available_at correcta; explicación T−1 incorrecta | Regla exacta correcta; explicación T−1 contiene una corrección textual confusa y un día incorrecto |
| Entidades repetidas | Permite compartir clientes, pero añade sensibilidad por grupos y agrupación interna sin necesidad demostrada | Evita GroupKFold por defecto; propone diagnóstico opcional |
| Fit/tuning dentro de desarrollo; test aislado | Cubierto en el diseño general | Cubierto en el diseño general |
| Outcomes excluidos y tickets agregados | Cubierto | Cubierto |
| Métricas mensuales / K provisional / causalidad | Cubierto; no confunde riesgo con efecto de retención | Cubierto; no confunde riesgo con efecto de retención |
| Checks concretos sin métricas inventadas | Propone checks; estima 360 positivos en test usando promedio global, no conteos mensuales | Propone checks y deja positivos por mes como no determinables |
| Definiciones provisionales y ausencia de aprobación | Cubierto | Cubierto |

No se usa score compuesto. Esta tabla es juicio semántico del asistente sobre un único caso, complementado con checks objetivos.

## Correcciones verificadas

1. Para scoring **2025-07-01**, el snapshot **2025-06-01** cubre junio y madura **2025-07-08**. No madura el mes posterior ni el día 7. El último snapshot entrenable al scoring es mayo, disponible desde 2025-06-08. La regla `label_available_at <= training_timestamp` evita depender de una frase ambigua.
2. Para validar **2024-10-01**, hay 7 meses entrenables: febrero–agosto. La propuesta baseline de train mínimo 8 meses desde ese fold es inconsistente. Si se exige 8, comenzar en noviembre. El treatment empieza en septiembre con febrero–julio: 6 meses, consistente.
3. Las 972 labels pendientes corresponden a enero de 2026. Sigue siendo incorrecto convertirlas en negativas incluso si ya consta alguna cancelación individual.
4. La frase «mes siguiente» del caso podía resultar ambigua. La ventana fuente siempre fue `[prediction_timestamp, window_end_exclusive)`. Se aclaró la documentación vigente a «mes calendario que comienza al scoring»; los inputs originales de la comparación se conservaron en `inputs/`.

Evidencia nueva, posterior a la ejecución: `../../analysis/outputs/temporal-checks.json`. Esta evidencia no se añadió retroactivamente a los runners.

## Eficiencia observada

| Ejecución | Duración | Coste registrado por el CLI |
|---|---:|---:|
| Baseline | 79,80 s | USD 0,1371 |
| Treatment | 82,21 s | USD 0,1840 |

Son mediciones de estas dos ejecuciones; no estimaciones de coste futuro ni significancia estadística. El treatment añade estructura y es más cuidadoso con algunos límites, pero persiste el error temporal y no hay evidencia repetida de ventaja.

## Decisión recomendada

Mantener el estado experimental. Corregir los diseños propuestos mediante la regla de disponibilidad y review humana antes de modelar. Repetir con otros casos y contextos, y solicitar revisión independiente antes de usar esta comparación como evidencia canónica del Foundry. Conservar hallazgos localmente; no crear automáticamente una skill de churn.
