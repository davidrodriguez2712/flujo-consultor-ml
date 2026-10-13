# Diagnosis preparado para revisión

Framing aprobado por David mediante «aprobado». Diagnosis y data-quality siguen pendientes.

## Artefactos a revisar

- `reports/dataset/dataset-understanding-2026-10-08.md`: grain, claves, missing, joins y riesgos.
- `reports/validation/validation-design-2026-10-08.md` y `validation/validation_design.yaml`: rangos, cutoffs, features y métricas.
- `reports/leakage/leakage-audit-2026-10-08.md`: mecanismos confirmados, riesgos y aspectos no determinables.
- `data/data_contract.yaml`, `evidence/findings.md` y `analysis/outputs/diagnosis-checks.json`: contrato y evidencia.

## Decisiones propuestas

Train development al2025-01-01; validation enero–febrero; selección al2025-06-15. Refit final al2025-07-01, scoring julio–septiembre y evaluación al2026-01-15. Modelo fijo en el periodo final. Labels disponibles al cutoff, join1:1 por solicitud, features admisibles declaradas y bins de calibración prefijados.

289 clientes son compartidos entre train final y concedidas finales: permitido para recurrentes, reportar nuevos por separado. No dar por independiente cada solicitud para estimar incertidumbre. No se agregó prevalencia de holdout ni se calcularon métricas predictivas; sí hubo checks globales de calidad sobre targets, por lo que no hay blinding por control de acceso.

## Límite operacional

El ranking con todas las solicitudes de un mes es un benchmark retrospectivo. No demuestra que esas revisiones puedan ejecutarse antes de aprobar/desembolsar. Para una política real online faltan reglas de llegada, presupuesto restante y momento de revisión; este fixture no estima ese impacto.

## Siguiente tarea tras aprobación

Congelar contrato de ejecución, código/configuración del baseline y reglas de evaluación antes de observar métricas finales; verificar con tests y auditoría de pipeline; ejecutar development y preparar su gate. No hay entrenamiento realizado ni nuevas llamadas API.
