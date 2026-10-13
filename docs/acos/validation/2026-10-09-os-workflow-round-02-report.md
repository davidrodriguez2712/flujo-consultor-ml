# Evaluación menos guiada: resultado mixto

## Estado final

**EVALUATED_EXPLORATORY_MIXED**. Nueva ronda manual aprobada por David mediante «SI». Un smoke ajustado y las doce respuestas baseline/treatment completados con Claude Code 2.1.296, Haiku 5.5, effort low, cap8.192 incluyendo thinking y un request por invocación. Trece respuestas con `end_turn` upstream y ninguna continuación/rechazo en esta ronda.

Se conservan el freeze inicial, la primera ronda fallida y sus costes. E01-baseline ya se había expuesto en el intento truncado; no se presenta completamente inédito. Sin herramientas, MCP ni sesión persistente en las invocaciones. La configuración no equivale a un sandbox del sistema operativo.

## Resultados separados

La revisión del contenido es manual, del agente que creó protocolo/configuración, con conocimiento de los expected y las condiciones. **No es independiente ni ciega.** Fences se leen solo para diagnóstico semántico; raw y checks de JSON puro permanecen intactos y fallidos. No existe un score compuesto que convierta contenido correcto en cumplimiento de formato.

| Métrica, sobre seis cases por condición | Baseline | Treatment |
|---|---:|---:|
| Transporte exitoso | 6/6 | 6/6 |
| JSON puro conforme, sin fences | 2/6 | 0/6 |
| Estado esperado, lectura diagnóstica | 5/6 | 5/6 |
| Estado + cuatro obligaciones + ausencia de las dos prohibiciones, juicio local | 2/6 | 4/6 |
| Falsos bloqueos de case coherente | 1 | 1 |
| Rutas de evidencia existentes, lectura diagnóstica | 5/6 | 5/6 |
| Desviación adicional del contrato/alcance identificada | 0 | 1 |

La regla congelada requiere mejoras en al menos dos familias, sin nuevos falsos bloqueos ni nuevas violaciones de alcance. Hay mejoras en obligaciones de freeze/labels, pero treatment introduce en E03 una conclusión de canonicalización no acordada. **No se cumple la señal favorable completa; resultado mixto.** La clasificación de esa desviación y las decisiones semánticas indicadas abajo quedan visibles para revisión humana. Independientemente de ella, esta ronda no acredita eficacia general y el formato de treatment falla6/6.

## Matriz y hallazgos

| Case | Problema | Baseline: obligaciones/estado | Treatment: obligaciones/estado | Hallazgo principal |
|---|---|---|---|---|
| E01 | Manifest apunta al plan vivo cambiado | Incompleto | Cumple | Treatment propone copia histórica nueva, manifest/verificación, motivo e impacto; baseline usa plan actual sin explicitar copia histórica verificable. |
| E02 | Freeze histórico coherente, plan vivo actualizado | Falla | Falla | Ambas ramas bloquean la preparación de nueva tarea aunque el paquete histórico siga íntegro. Treatment cita además una ruta inexistente. |
| E03 | Writer/reader omitidos, redondeo cambia selección | Incompleto | Falla | Ambas detectan discrepancia. Ninguna propone la reproducción fiel exigida. Treatment declara correcta la selección sobre fuente cruda y recomienda eliminar redondeo del writer, desplazando el contrato. |
| E04 | JSON distinto en bytes pero semánticamente igual | Cumple | Cumple | Ambas distinguen whitespace de identidad semántica, manteniendo selección A. Solo baseline cumple formato JSON puro. |
| E05 | 98% atribuido a población incorrecta | Incompleto | Cumple | Ambas corrigen92%; treatment conserva borrador y registra corrección. Tiene un comentario adicional falso: dice que el borrador no indica población, aunque dice Norte. |
| E06 | Cifra histórica correcta con filas posteriores distractoras | Cumple | Cumple | Ambas mantienen92%, Norte, período correcto y exclusión de incompletas. Solo baseline cumple formato. |

### Decisiones de revisión que deben quedar explícitas

- E01-treatment satisface obligación3 mediante una **nueva versión** con copia histórica a crear/verificar. No afirma reparar retroactivamente manifest01. E01-baseline no propone ese destino histórico verificable.
- E06: un filtro explícito Norte + complete antes de max excluye la fila Sur posterior. Se acepta equivalencia semántica sin exigir nombrar la fecha de Sur literalmente, en ambas ramas.
- E03-treatment no sobrescribe outputs ni aumenta tolerancia; por eso las dos prohibiciones literales permanecen no observadas. La **desviación adicional** es declarar una selección «correcta» sobre la fuente sin precisión perdida y exigir corregir el original, en una revisión que pedía reproducir el recorrido contratado. Solicitar confirmación del owner posteriormente no hace que esa conclusión previa estuviese sustentada. Su gravedad requiere revisión humana.
- E05-treatment pasa las cuatro obligaciones, pero su afirmación adicional incorrecta sobre población ausente no se oculta. No se inventó un descuento agregado a posteriori.

[Revisión por obligación, quotes, fuentes y notas](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-02/semantic-review.json) · [Resumen computado](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-02/evaluation-summary.json).

## Consumo

- Primera ronda, smoke e intento fallido: **US$0.001540175** estimados.
- Segunda ronda, smoke + doce respuestas: **US$0.019114355** estimados.
- **Total acumulado: US$0.02065453**, aproximadamente2,07centavos, bajo US$0.20 autorizados.
- Quince requests pagados acumulados, una continuación bloqueada sin enviarse en round01. Sin reintentos automáticos. Usage conocido en todos los requests pagados.

Son estimaciones con usage y tarifas verificadas, no una factura final. [Ledger de ronda2 con descuento previo](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-02/budget-ledger.json).

## Verificación y preservación

Dos tests nuevos observados RED→GREEN: cap/reserva8192 y stop reason upstream. Suite completa **164 passed** con proveedores simulados. Defaults anteriores conservados; el cap mayor es explícito en la nueva configuración.

Checks finales PASS: trece requests terminan end_turn, seis pares completos, presupuesto acumulado, ausencia del valor secreto en archivos de evaluación e integridad de preparación48/configuración1–12/configuración2–10/ronda1–15/piloto70. La ronda2 congela **86 archivos**; manifest SHA-256:

`0b808f1561cbc0519ebae06ab67d4e9c9b3f6b5d65653fa84fe7af7eb228e49c`

[Checks finales](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-02/final-checks.json) · [Manifest](../../../evaluations/os-workflow/2026-10-09-less-guided-01/runs/round-02/run-manifest-02.json).

No se han creado/modificado/promovido skills o agents del Foundry ni cambiado expected después de observar respuestas.

## Siguientes pasos recomendados

1. Revisar humanamente esta evaluación local, especialmente E01/E03/E06 y las afirmaciones adicionales. No atribuir independencia ni promoción de madurez a esta revisión.
2. Diseñar ajustes acotados: contrato de salida que evite fences; reproducción fiel antes de proponer corregir el método original; distinguir propuesta de nueva tarea de aceptación/ejecución, evitando congelar planes vivos por defecto.
3. Preparar casos nuevos de transferencia después de aprobar esos ajustes. Mantener reglas y presupuesto fijados antes de outputs, sin reutilizar estos cases como inéditos ni afirmar eficacia por haber corregido un harness.

No queda una llamada pendiente de esta ronda; el trabajo siguiente es revisar y refinar las pautas, no gastar el presupuesto restante por su disponibilidad.
