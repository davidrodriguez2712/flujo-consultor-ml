# Protocolo fijo de evaluación final

## Autorización y configuración

David aprobó Execution después del resultado de development y autorizó continuar con refit/evaluación final. Se conserva la configuración: mismo baseline/código de modelo, cinco features,600iteraciones,learning_rate0.05,L2=0.01, bins prefijados yK100. Único refit con labels disponibles al2025-07-01; modelo fijo durante scoring julio–septiembre2025. Outcomes de evaluación disponibles al2026-01-15.

Freeze antes del run principal: runner nuevo, baseline intacto, policy y cinco CSV; hashes de contratos y snapshots documentados adicionalmente. Runner verifica código/policy/inputs; checks de closure verifican también artefactos/contratos. No reintentar para mejorar resultados ni elegir otra configuración a partir del holdout.

## Evidencia y límites de evaluación

Modelo/referencia y900scores deben generarse antes de interpretar labels del scoring. El loader de train lee el CSV pero filtra elegibilidad antes de int(target). Labels de evaluación se cargan después de persistir predicciones en staging. QA previa de todo raw en Diagnosis incluyó relación target/columna posterior: no afirmar holdout ciego ni labels inaccesibles.

Las pruebas de integración del wrapper usan fixtures manuales, no calculan métricas del periodo final real. Tampoco usar el generator conocido para introducir propensión latente como feature.

Brier/ROC-AUC/calibración/segmentos en concedidas maduras; ranking de esa población separado de todas las solicitudes. Metrics de todas no identificadas si faltan outcomes según denominador. El benchmark mensual es retrospectivo, sin política online ni efecto de revisión. Mejora puntual no significa significancia, generalización real o eficacia de skills.

## Comando reproducible

Desde la carpeta del piloto, usando output nuevo:

```sh
python analysis/credit_final.py --freeze-file reports/final-validation/final-freeze.json --output analysis/outputs/final-replay
```

Los outputs almacenan timestamps; los modelos/scores/resultados deben reproducirse con idénticos inputs/configuración. No invoca APIs ni instala dependencias. Después de la ejecución, revisar cinco gates de Validation antes de Delivery.
