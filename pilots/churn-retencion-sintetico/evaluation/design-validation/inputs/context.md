# Contexto del piloto

El usuario eligió churn / retención y autorizó crear datos porque no dispone de un dataset. Se usa una empresa ficticia de suscripciones para probar ACOS; no representa demanda ni comportamiento comercial real.

## Decisión propuesta para revisión

Cada comienzo de mes, proponer qué clientes activos priorizar para que el consultor revise una posible acción de retención. Supuesto operativo: capacidad de 50 contactos/mes. KPI analítico propuesto: Precision@50 y Recall@50 por mes; MRR en riesgo como contexto, no como beneficio incremental.

## Alcance autorizado

Generar datos y preparar el piloto supervisado; producir checks, documentación y evidencia de las capacidades utilizadas. No ejecutar campañas ni simular una aprobación humana de gates. No promover capacidades en Foundry.

## Definiciones del laboratorio

Churn es una cancelación en el mes calendario siguiente al scoring. Cada snapshot representa un cliente activo al inicio del mes. La label se conoce al cerrar el mes más 7 días; su disponibilidad debe gobernar el entrenamiento. Los mismos clientes pueden repetirse entre meses si reproduce el scoring mensual.

## Pendientes de revisión humana

Aceptar o ajustar el caso, capacidad, KPI, definición de churn y entregable; designar reviewer. Estos son supuestos de laboratorio propuestos por el asistente, no instrucciones de una empresa real.
