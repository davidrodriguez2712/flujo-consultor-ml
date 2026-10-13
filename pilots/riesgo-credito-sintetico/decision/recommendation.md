# Recomendación — propuesta para aprobar Delivery

## Acción recomendada

David: conservar el prototipo, los resultados y el paquete de evidencia como aprendizaje del piloto sintético. La decisión operacional de priorizar todas las solicitudes está parcialmente respondida. Antes de una política real, definir momento de revisión, población/outcome observables y una evaluación adecuada de esa política.

## Fundamento

Brier final 0,102487 frente a 0,116530 y ROC-AUC 0,752283 en 447 concedidas maduras. La mejora puntual no implica calibración certificada; bins pequeños/desajustes y una población seleccionada acotan la interpretación.

Top-100 de todas las solicitudes: solo 22–26 % tienen outcome observado, por lo que Precision/Recall/Lift globales no se identifican. El ranking mensual es retrospectivo; no se evalúa revisar antes de la decisión de conceder. No identificar beneficio de intervención a partir de riesgo predictivo.

## Condiciones para siguiente trabajo

1. Owner de negocio real, decisión/momento y política de asignación definidos.
2. Contrato de datos que distinga outcomes observables de contrafactuales; sin completar rechazadas como negativos.
3. Protocolo con métricas/comparador/supuestos revisado antes de ejecutar.
4. Datos/evaluación independientes para una versión futura; no ajustar con el holdout observado.

No estimar ahorro ni ROI sin inputs y evidencia adecuados. La autoridad de aprobar acciones reales pertenece al owner correspondiente; este documento no asigna permisos.

## Entregables relacionados

[Decision memo](../delivery/decision_memo.md), [informe analítico](../delivery/analytical_report.md) y [validación final](../validation/model_validation.md). Revisión humana de Delivery pendiente; luego handoff.
