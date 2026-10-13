# Framing preparado para revisión

Discovery aprobado por David mediante «continúa», después de presentar el paquete y su gate pendiente. Se registró la evidencia y se avanzó explícitamente a Framing.

## Decisiones propuestas

- Brier score como métrica primaria, con predictor constante de referencia; ROC-AUC y calibración secundarias.
- Evaluación limitada a créditos concedidos con labels maduros; sin resultados identificados para rechazadas.
- Ranking por riesgo para revisión humana, hasta 100 solicitudes por mes, empate por ID. Separar evaluación offline y propuesta sobre todas las solicitudes.
- Reportar resultados desfavorables y no estimar ahorro sin evidencia causal.

Leer `framing.yaml`, `metrics.yaml`, `scope.md` y `acceptance.md` de esta carpeta. No se han aprobado estas propuestas ni se ha entrenado un modelo. El siguiente paso, tras revisión, es Diagnosis con understand-dataset, diseño de validación y auditoría de leakage dentro de sus alcances.
