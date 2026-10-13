# Transferencia: evaluación inconclusa con defecto de preparación

## Estado

**EXPLORATORY_INCONCLUSIVE_PREPARATION_DEFECT**. David autoriza hastaUS$0.10 adicionales mediante «si aprobado». Smoke Markdown y doce respuestas completados;13requests HTTP200, todosend_turn, usage conocido, sin retries ni rechazos. Claude Code2.1.296, Haiku5.5, effortlow, cap8192, prompt neutral explícito igual en todas las celdas.

Revisión manual del autor de fixtures/controles; no independiente ni ciega. La revisión local y el diagnóstico no reparan raw ni convierten automáticamente formato inválido en PASS. No hay promoción de madurez ni eficacia general acreditada.

## Defectos de preparación y exclusión simétrica

**T02 pricing queda excluido de inferencia en ambas condiciones.** Los seis pares se conservan, pero solo cinco son comparables para análisis descriptivo; no se reemplazan ni reejecutan outputs. Expected READY original y checks intactos.

1. Fixture ambiguo: volumen e ingresos200.000 fijos, margen bruto50.000→55.000 y etiqueta “escenario de pricing” sin mecanismo documentado. Coste implícito150.000→145.000. Ambas respuestas cuestionan esa definición y devuelven MUST_CORRECT; ese diagnóstico puede ser legítimo, por lo que no sirve para medir falsos bloqueos. No se demuestra que todo escenario de precios con ingreso agregado fijo sea imposible; falta definir la mecánica en este expediente.
2. Checker Markdown demasiado restrictivo: exige que toda sección Estado sea solo el token. T02-treatment añade explicación después de MUST_CORRECT, aunque el contrato público permite prosa dentro de secciones. Su FAIL automático se conserva; no se atribuye inequívocamente al modelo ni se recalifica con checker modificado. T02-baseline tiene formatoPASS y estado distinto al oracle.

T02-baseline además atribuye específicamente al borrador una afirmación de precios que este no contiene literalmente; se deja visible como nota de soporte, sin convertir un par defectuoso en una medición de eficacia. La tarea/contexto sí lo llaman escenario de pricing.

[Registro de defecto](../../../evaluations/os-workflow/2026-10-09-transfer-01/runs/round-01/preparation-defect-review.json).

## Cinco pares comparables

| Métrica | Baseline | Treatment |
|---|---:|---:|
| Formato conforme |4/5|5/5|
| Estado esperado, lectura diagnóstica |5/5|5/5|
| Contenido conforme a cuatro obligaciones, revisión local |4/5|4/5|
| Formato y contenido conformes |3/5|4/5|
| Falsos bloqueos/violaciones de alcance observados |0/0|0/0|

| Caso | Resultado y límite |
|---|---|
|T01 churn/API|Ambas cumplen shortlist, JSON puro y límites causales.|
|T03 inventario/IDs|Ambas proponen reproducción fiel en destino nuevo, sin canonicalizar source.|
|T04 forecast/variante|Ambas calculan bruto120/neto100 y separan versiones; piden confirmaciones adicionales potencialmente redundantes, registradas para revisión.|
|T05 crédito/task|Ambas permiten redactar y bloquean solo ejecución dependiente. Ambas fallan obligación2: indican cómo redactar después, sin entregar task concreto con outputs y revisión.|
|T06 retención/campaña|Ambas bloquean envío y permiten preparación. Baseline tiene dos findings como strings con texto JSON en vez de objetos: schemaFAIL. Treatment cumple schema. El contenido de esos strings se lee solo para diagnóstico manual, sin reconstruir respuesta conforme.|

Todos los checks sobre las seis respuestas completas dan formato5/6 para cada condición: baseline fallaT06, treatment fallaT02 según checker congelado. La tabla parcial no reemplaza ese dato ni oculta T02. T06 mejora formato fuera de la familia de formato; no implica mejora de contenido en continuidad ni cumplimiento de señal en dos familias.

Regla congelada favorable **no satisfecha** y cobertura planeada incompleta. No hay mejora incremental de contenido en los cinco pares; mejora puntual de schema T06. Una repetición no estima variabilidad. No comparar porcentajes con el estudio anterior como si fueran el mismo test.

### Juicios de revisión visibles

T05obligación1 admite reconocimiento estructural/alcance y no invalidación del histórico sin exigir cómputo SHA con tools deshabilitadas. “No se verificaron hashes” no equivale a freeze inválido. La frase baseline “No es posible verificar... a partir del expediente” es demasiado absoluta y queda registrada; no se convierte en prueba de que faltan bytes ni se exige afirmación criptográfica inventada. Req2 falla por sustituir borrador por instrucciones futuras, no por filenames o wording. Ambas ramas reciben la misma interpretación.

T04obligación4 acepta límites equivalentes sobre calidad predictiva/elección de target, sin exigir frase exacta “no demuestra superioridad”. Confirmaciones adicionales del plan/contrato son cautela potencialmente redundante, no prohibición de cambio autorizado, pues ambas preparan propuestas ahora. Estas decisiones son revisables humanamente.

[Revisión por obligación y citas](../../../evaluations/os-workflow/2026-10-09-transfer-01/runs/round-01/semantic-review.json) · [Resumen](../../../evaluations/os-workflow/2026-10-09-transfer-01/runs/round-01/evaluation-summary.json).

## Coste y preservación

Nueva ronda: **US$0.02088035** estimados; límite autorizadoUS$0.10. Estudio anteriorUS$0.02065453. Total ambos estudios: **US$0.04153488**. Son estimaciones de usage y tarifas verificadas, no factura final ni impuestos. No queda llamada pendiente; saldo nominal no habilita nuevas rondas o retries.

Preflight inicial se detuvo por incluir un pycache generado al recorrer snapshots. Cero requests y clave no cargada en ese intento. Corrección local compara los archivos listados en manifest, sin alterar código aprobado o freeze. No fue retry del proveedor. La receta operativa de revisión corrigió una selección de cita literal antes de generar evidencia; no cambió juicios ni outputs.

Checks finales PASS:13end_turn, doce payloads exactos, mismo system prompt, budget, usage conocido, quotes/rangos contra raw, secreto exacto ausente e integridad de **316 archivos** anteriores (253históricos+50preparación+13configuración). Código/tests permanecen los verificados con182PASS; no se reejecutó suite ni se cambió producto durante calls. Foundry intacto.

Freeze de run: **86 archivos**, SHA-256 `0cef7918311a6902d3709bd607d7bdb045b9b94dd9ff73393a5ab4c2fffdbfd5`.

[Ledger](../../../evaluations/os-workflow/2026-10-09-transfer-01/runs/round-01/budget-ledger.json) · [Checks](../../../evaluations/os-workflow/2026-10-09-transfer-01/runs/round-01/final-checks.json) · [Manifest](../../../evaluations/os-workflow/2026-10-09-transfer-01/runs/round-01/run-manifest-01.json).

`round-status.json` conserva el estado histórico de recolección pendiente de revisión; `evaluation-summary.json` registra el estado posterior autorizado de esta evaluación.

## Siguiente trabajo propuesto

Corregir contrato/checker Markdown y diseñar un fixture de pricing inequívoco en versión nueva; reforzar entrega concreta del borrador de task sin añadir gates innecesarios. Primero revisión local del diseño y tests, preservando estos inputs/outputs. T02 expuesto no vuelve a ser inédito. Configuración y presupuesto nuevos antes de otras llamadas; no gastar saldo por existir. Revisión humana separada de los juicios anteriores recomendable antes de atribuir mejoras a capacidades del Foundry.
