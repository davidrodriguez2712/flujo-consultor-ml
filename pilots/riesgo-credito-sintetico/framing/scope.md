# Scope propuesto — pendiente de revisión de Framing

## Incluido

Baseline reproducible de riesgo condicionado a créditos concedidos, usando únicamente información disponible al scoring. Validación temporal con disponibilidad de labels al entrenar, control de clientes repetidos, preprocesamiento fit en train y holdout congelado antes de observar métricas. Discriminación, calibración y ranking con capacidad mensual; informe y decision memo.

## Dos poblaciones que no se mezclan

1. **Evaluación offline:** créditos concedidos y maduros. Se calcularán métricas solo para esa población y se mostrará selección por mes con su K efectivo propio.
2. **Propuesta operacional:** todas las solicitudes del mes. Ordenar scores no demuestra que estén calibrados para rechazadas. Se reportarán elegibles, seleccionados y cobertura de labels; no se calcularán Precision/Recall/Lift globales si faltan outcomes. El ranking sigue siendo una simulación para revisión humana.

El modelo aprendido en concedidas estima una asociación en esa población seleccionada. No identificarlo automáticamente como PD válida para todos los solicitantes. Revisión manual no implica que hubiera cambiado mora o pérdida.

## Fuera del alcance aprobado

Concesión automática, pricing, política crediticia real, reject inference mediante labels inventados, calendario detallado de cuotas, LGD/EAD reales, cálculo de pérdidas evitadas, frontend, despliegue y promoción de capacidades del Foundry.

## Trazabilidad

Perfil y módulos compilados permanecen intactos. Los contratos de Framing detallan el scope aprobado como propuestas revisables; sus métricas y política de ranking requieren aprobar este gate. Datos de laboratorio: `data/raw/manifest.json` y `data/dictionaries/README.md`.
