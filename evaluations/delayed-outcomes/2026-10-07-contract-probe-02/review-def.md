# Review independiente — D/E/F

Reviewer: /root/temporal02_outputs_def. Contexto nuevo, solo lectura; task, protocolo, rúbrica y expected leídos antes de outputs. No consultó conclusiones del autor ni ejecutó servicios. Registro consolidado de su devolución; no revisión humana externa.

| Caso | Rama | Rep | Instantes | Certificación / unknown | Congruencia | Preguntas | Autoridad textual |
|---|---|---:|---|---|---|---|---|
| D | baseline | 1 | PASS | PASS | PASS | PASS | PASS |
| D | baseline | 2 | PASS | PASS | PASS | PASS | PASS |
| D | treatment | 1 | PASS | PASS | PASS | PASS | PASS |
| D | treatment | 2 | PASS | PASS | PASS | PASS | PASS |
| E | baseline | 1 | PASS* | PASS* | UNCLEAR* | FAIL | PASS* |
| E | baseline | 2 | PASS | PASS | PASS | FAIL | PASS |
| E | treatment | 1 | PASS | PASS | PASS | PASS | PASS |
| E | treatment | 2 | PASS | PASS | PASS | UNCLEAR | PASS |
| F | baseline | 1 | PASS | PASS | PASS | PASS | PASS |
| F | baseline | 2 | PASS | PASS | PASS | FAIL | PASS |
| F | treatment | 1 | PASS | PASS | PASS | PASS | PASS |
| F | treatment | 2 | PASS | PASS | PASS | PASS | PASS |

* E baseline1 contiene razones legibles pero JSON inválido; PASS del texto no otorga acierto de decisiones ni disponibilidad omitida. Mantener sus dos filas no evaluables en el denominador.

## Hallazgos

Las razones legibles reconocen D1 certificado temprano, D2/E1 provisionales hasta 2025-07-04, E2 con certificación desconocida, y F1 con equivalencias de offsets e igualdad. No encontró razones temporales falsas ni expected ambiguos. Baseline: doce razones legibles, dos de ellas en output no evaluable. Treatment: doce razones evaluables.

- [E baseline1](runs/E/baseline/1/result.txt), línea 7: `"label_availability_at_training",` omite dos puntos y valor. No reparar ni reconstruir disponibilidad desde reason. El JSON es inválido incluso sin fences.
- [E baseline2](runs/E/baseline/2/result.txt), pregunta: «los datos extraídos el 06-20 no pueden haber alimentado un entrenamiento del 06-15». Confunde una auditoría de disponibilidad histórica con haber entrenado usando el archivo posterior. No cambia las clases correctas que devolvió.
- [F baseline2](runs/F/baseline/2/result.txt), pregunta: «sus labels estaban disponibles antes de ambos instantes». F1 está disponible exactamente al entrenar. La misma pregunta menciona igualdad y reason la calcula correctamente; es un error localizado en la pregunta.

Tres outputs baseline reabren timestamps suministrados: E1, E2 y F2. E treatment2 plantea como hipótesis si existe otra fecha certificada para E1: pertinencia UNCLEAR, porque la regla ya permite decidir. La rúbrica permite aclarar hipótesis; no recalificarlo como falso ni fallo temporal. Preguntas sobre certificación/historial de E2 son pertinentes.

Fences: tres baseline y uno treatment en D/E/F; uno de esos baseline además es JSON inválido. Cero admisiones indebidas o pérdida de válidos entre decisiones evaluables; no usar la respuesta malformada para afirmar ausencia de errores.

Verificó hashes de payload/request y correspondencia con payload congelado, raw/result, session ID/model/coste de metadata y precedencia de started_at respecto de frozen_at. Configuración efectiva restante sigue desconocida.

Conclusión del reviewer: menos preguntas problemáticas y mejor entrega estructurada en treatment en este subconjunto, con pocas repeticiones. No prueba eficacia global, autoriza promoción ni sustituye revisión humana externa.
