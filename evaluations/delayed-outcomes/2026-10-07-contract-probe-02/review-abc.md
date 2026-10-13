# Review independiente — A/B/C

Reviewer: /root/temporal02_outputs_abc. Contexto nuevo, solo lectura; task, protocolo, rúbrica y expected leídos antes de outputs. No ejecutó servicios ni consultó tally del autor. Registro consolidado de su devolución; no revisión humana externa.

| Caso | Rama | Rep | Instantes | Certificación | Features | Incertidumbre | Congruencia | Preguntas | Autoridad |
|---|---|---:|---|---|---|---|---|---|---|
| A | baseline | 1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| A | baseline | 2 | PASS | PASS | PASS | PASS | PASS | FAIL | PASS |
| A | treatment | 1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| A | treatment | 2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| B | baseline | 1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| B | baseline | 2 | PASS | PASS | PASS | PASS | PASS | FAIL | PASS |
| B | treatment | 1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| B | treatment | 2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C | baseline | 1 | PASS | PASS | PASS | PASS | PASS | FAIL | PASS |
| C | baseline | 2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C | treatment | 1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| C | treatment | 2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## Hallazgos

Doce razones por condición: ninguna falsa. A separa labels certificados en extracción y disponibilidad histórica; B admite igualdad y excluye +1 segundo; C reconoce feature futura y disponibilidad desconocida. No encontró ambigüedad material en expected ni intervalos inventados. Todos los gates NEEDS_REVIEW. Menor explicitud de certificación en baseline C no implica falsedad: la fuente suministrada certifica la fecha.

Tres preguntas redundantes de baseline, una por output:

- [A baseline2](runs/A/baseline/2/result.txt): «Confirmar que el entrenamiento histórico debe evaluarse con la información disponible al 2025-09-01 y no a la fecha de extracción». La tarea ya lo fija.
- [B baseline2](runs/B/baseline/2/result.txt): pide «confirmar que el entrenamiento histórico usa solo información disponible hasta training_timestamp». El escenario es una auditoría ficticia, no entrenamiento ejecutado.
- [C baseline1](runs/C/baseline/1/result.txt): «¿Es correcto este orden, o el entrenamiento debería ejecutarse con datos extraídos después de su fecha?». El snapshot posterior está provisto; la pregunta por features desconocidas de C2 sí es pertinente.

Fences: A baseline2, B treatment1, C treatment1. Son incumplimientos de formato estricto, no errores de clasificación; los payloads internos se evaluaron por diagnóstico tolerante.

Verificó payload/request hashes y correspondencia con payload congelado, raw/result y metadata de las doce llamadas. La prueba acredita coherencia local, no flags efectivos que el proveedor no expone.

Conclusión del reviewer: treatment evita tres preguntas redundantes y explicita ejes, pero A–C no muestran reducción de errores temporales porque ambas ramas aciertan. Treatment tiene un fence adicional en este subconjunto. Sin autoridad para promover o afirmar eficacia general.
