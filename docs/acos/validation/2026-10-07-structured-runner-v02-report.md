# Check técnico: runner temporal 0.2.0

Fecha local: 2026-10-07. Implementación y dos calls nativos autorizados. Resultado: **check técnico satisfactorio en el alcance ejecutado**. No constituye una nueva evaluación de eficacia ni una promoción del Foundry.

## Qué cambió

Se añadió [temporal_runner.py](../../../scripts/evaluations/temporal_runner.py) y un [schema común 0.1.0](../../../schemas/temporal-audit-0.1.0.schema.json). Se conservan por separado el envelope nativo, su objeto `structured_output`, la validación local y la comprobación externa del contenido. La utilidad se ejecuta desde el checkout; no modifica los comandos instalados de ACOS. Consultar [uso y límites](../evaluation-contracts/structured-runner.md).

No existe fallback desde `result`, reparación ni reintento del runner. El objeto inválido se archiva. La revisión independiente del código detectó un fallo de escritura con Unicode inválido; cuatro regresiones fallaron antes de la corrección y pasaron después. El reviewer confirmó que no quedaban Critical/Important para estos calls. Es revisión por otro agente, no revisión humana externa.

## Diseño conservado antes de ejecutar

Se reutilizaron los payloads baseline/treatment y expected del case E de la ronda temporal 02, sin cambiar sus bytes. Se congelaron ocho archivos con hashes y timestamp local antes del primer call. Expected quedó fuera de ambos payloads y del runner; solo el checker externo lo consultó después.

[Evidencia del check](../../../evaluations/engineering/2026-10-07-structured-runner-v02-check/protocol.md), [preregistro](../../../evaluations/engineering/2026-10-07-structured-runner-v02-check/preregister.json). Estos hashes no acreditan cronología externamente.

## Resultados nativos

Claude Code `2.1.293`; modelo solicitado y reportado `claude-sonnet-5-5`. Schema idéntico para ambas condiciones.

| Control | Baseline | Treatment |
|---|---:|---:|
| Runtime exitoso | Sí | Sí |
| Objeto nativo presente | Sí | Sí |
| Validación local `schema_conformant` | Sí | Sí |
| Modelo coincide | Sí | Sí |
| Campos correctos, checker externo | 6/6 | 6/6 |
| Decisiones correctas | 2/2 | 2/2 |
| Gate | NEEDS_REVIEW | NEEDS_REVIEW |
| Wall time | 8.343 s | 8.495 s |
| Turns reportados | 2 | 2 |
| Coste reportado por CLI | USD 0.065178 | USD 0.0686082 |

Coste total reportado: **USD 0.1337862**, estimación del CLI, no factura. Dos invocaciones CLI no equivalen necesariamente a dos requests internos. Effort medium y restricciones se solicitaron en argv; su aplicación efectiva no está confirmada por el envelope.

`schema_conformant` incluye Pydantic estricto y controles locales adicionales de unicidad de IDs, texto no vacío y Unicode válido. El runner conserva `content_validation=NOT_RUN`: los resultados de contenido proceden del checker externo, archivado con su argv y exit code. No confundir un código 0 del checker con corrección: se inspeccionaron sus campos de resultado.

## Revisión semántica del autor

Ambas respuestas distinguen E1, cuyo cero es provisional y cuya certificación ocurre después del entrenamiento, de E2, cuya regla de certificación es desconocida. Las razones son coherentes con el case; no se observó admisión inválida ni aprobación automática del gate.

Las preguntas pertinentes de E2 piden reglas e instantes de certificación. Baseline añade una confirmación redundante de la regla explícita de E1; treatment pregunta si la reconstrucción histórica con entrenamiento anterior a extracción es intencional. Esta última no contradice el case, pero no es necesaria para resolverlo. La revisión semántica es del autor y no acredita superioridad del treatment.

## Verificación

- Suite local del producto y runner: **112 passed**.
- Suite ampliada con piloto y checker/runner congelados de la ronda 02: **138 passed**.
- Pruebas nuevas del runner: **15 passed**, con revisión independiente posterior a la corrección Unicode.
- Integridad: **424 archivos** de las cuatro evaluaciones anteriores y **48 entradas protegidas** del piloto conservan sus hashes y tamaños pertinentes.
- Ocho inputs congelados y hashes de artefactos de ambos calls verificados. [Resultado de integridad](../../../evaluations/engineering/2026-10-07-structured-runner-v02-check/integrity-check.json).

## Estado y siguientes pasos

Runner disponible para preparar futuras rondas. La ronda 02 anterior permanece cerrada; estos dos checks no recalifican sus outputs. El contrato temporal sigue propuesto y no se incorporaron capacidades al compiler ni al Foundry.

Recomendación: diseñar una nueva evaluación con cases inéditos, menos guiados y con positivos, negativos e información insuficiente; congelar expected y rubric antes de ejecutar con este runner. Acordar repeticiones y presupuesto de calls, y solicitar revisión humana de las conclusiones antes de decidir si hace falta un artefacto reutilizable. La ejecución nativa Windows y el piloto con datos reales siguen pendientes del proyecto general.
