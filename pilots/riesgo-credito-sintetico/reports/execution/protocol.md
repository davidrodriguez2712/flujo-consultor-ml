# Protocolo de development fijo

Estado: código/configuración revisados y congelados antes de la ejecución principal. Alcance autorizado: development; evaluación final no iniciada.

Regresión logística stdlib, cinco features, mediana/escala solo train,600iteraciones,learning_rate0.05,L2=0.01; sin tuning. Referencia de prevalencia. Las 1.248 filastrain deben tener scoring anterior y label disponible al2025-01-01. Las 298 filasvalidation tienen scoring enero–febrero2025 y labels disponibles al2025-06-15.

Métricas: Brier principal, ROC-AUC, bins fijos, reportes por mes y cliente conocido/nuevo, Top-K retrospectivo en concedidas. No decidir otro modelo o configuración con métricas finales. Compartir clientes en periodos es permitido; no son features. Si resulta desfavorable, conservar resultado.

Las pruebas de integración ejecutaron development en copias temporales del mismo generator/seed. No se usaron sus métricas para seleccionar parámetros. Este freeze precede el run principal, no todo acceso previo a datos o cálculos de QA. Tampoco hay blind holdout: raw disponible y usado para checks de calidad anteriormente.

El runner verifica codehash, policy y hashes de cinco CSV; la verificación de closure comprueba por separado los hashes de contratos/snapshots declarados en este freeze. El gate Execution requiere revisión humana después de observar el resultado.

Reproducción desde la carpeta del piloto:

```sh
python analysis/credit_baseline.py --freeze-file reports/execution/development-freeze.json --output analysis/outputs/development-replay
```

Usar output nuevo. No invoca LLM, no instala paquetes ni evalúa julio–septiembre. Entorno: Pythonstdlib; tests requieren pytest.
