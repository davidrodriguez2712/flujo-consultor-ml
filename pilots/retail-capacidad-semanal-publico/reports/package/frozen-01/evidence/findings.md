# Findings

## F-01 — Media de cuatro semanas mejora development

Métrica: WAPE de facturas UK por semana; población: facturas con filas calificantes. Development [2011-01-03, 2011-08-01), 30 semanas, 8.670 facturas. Baseline 0.18396770; media de cuatro semanas 0.15207612. Keys: método + cutoff. Fuente: reports/run-01/development_predictions.csv y strategy.json. Hecho retrospectivo, no efecto causal.

## F-02 — Final conserva subestimación

Opción elegida antes de calcular final: mean_previous_4_weeks. Final [2011-08-01, 2011-12-05), 18 semanas, 7.439 facturas; WAPE 0.13146928, MAE 54.33333333, bias -37.91666667 facturas/semana. No se comparó baseline final; no afirmar superioridad fuera de development. Fuente: reports/run-01/final_predictions.csv y result.json.

## F-03 — Última semana completa explícita

[2011-11-28, 2011-12-05): observado 608 facturas; forecast 556,5. La semana 2011-12-05 está parcialmente observada y excluida. Fuente/key: final_predictions.csv, method=mean_previous_4_weeks, cutoff=2011-11-28. Una copia de stress atribuyó 317,5 de 2011-08-01 al último período; QA detectó la discrepancia y conservó original y corrección separados.

## F-04 — Tres mejoras ejercitadas

Freeze de protocolo/plan conservado al actualizar documentos vivos; siete archivos de outputs idénticos en reproducción externa al checkout; QA detectó cifra válida atribuida al período incorrecto. Evidencia: reports/validation/freeze-check.json, reports/reproduction/reproduction-check.json y reports/qa/label-check.json. Ejecución guiada y determinista, sin control/treatment; no demuestra eficacia de skills o de agentes autónomos.
