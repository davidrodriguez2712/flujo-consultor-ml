# Contexto de negocio — laboratorio de riesgo de crédito

## Decisión y responsables

Priorizar solicitudes para revisión manual con capacidad de hasta 100 revisiones al mes. David revisa los gates del laboratorio. La concesión de crédito no se automatiza. Empresa y equipo ficticios; no existe un cliente real ni una política crediticia aplicable.

## Alcance aprobado

Datos sintéticos reproducibles; comprensión de datos; auditoría de leakage; validación temporal; baseline; discriminación, calibración y selección bajo capacidad; decision memo y handoff. Capacidades existentes del Foundry en uso provisional.

Target propuesto aprobado en el diseño: 30 días de mora alcanzados durante los primeros 90 días del crédito. Regla específica del fixture: label completa al día 97. Detalles y límites en `data/dictionaries/README.md`.

## Fuentes

`data/raw/`: cinco CSV con claves 1:1 y manifest de hashes. 7.200 solicitudes en 24 meses, enero 2024–diciembre 2025; extract 2026-01-15. Las cifras auditadas se presentan en `reports/discovery/discovery-review.md`.

## Límites que afectan la decisión

Solo los créditos concedidos y maduros tienen outcome. Calibración/discriminación en esa población no acreditan desempeño sobre todas las solicitudes. Solicitudes rechazadas sin label y pendientes deben permanecer sin target. Variables posteriores y joins por cliente pueden producir leakage/duplicación.

No se identifica ahorro causado por revisar ni efectos de una política nueva. El baseline y el ranking deberán explicitar población, cutoff, disponibilidad, capacidad y restricciones. Antes del modelado se fijarán métricas, aceptación y holdout sin observar resultados para ajustar decisiones.

## Entregables y continuidad

Informe analítico reproducible y decision memo con población, evidencia, límites y decisiones pendientes; runbook y feedback de capacidades al cerrar. Discovery está preparado para revisión: no se ha aprobado ni avanzado su gate.
