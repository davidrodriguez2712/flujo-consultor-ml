# Workflow común acotado para auditoría de leakage

Extracto literal del workflow OS: autoridad, cierre y escalamiento. Aplicar el contrato específico de case.md.

## Capacidad y autoridad

Que el harness pueda realizar una acción no autoriza a realizarla. La tarea declara alcance de lectura/escritura y herramientas. El agente puede inspeccionar fuentes autorizadas, producir borradores/artefactos en rutas acordadas y proponer decisiones. No debe:

- ampliar acceso, cambiar de cliente o mezclar contextos;
- cambiar unilateralmente alcance, KPI, población o contrato de datos;
- enviar mensajes, compartir un deliverable, publicar o cambiar sistemas remotos/producción sin autorización explícita;
- aprobar decisiones de negocio o promociones del Foundry por el consultor/usuario;
- presentar una inferencia, un supuesto o un resultado experimental como un hecho validado.

El reviewer puede revisar y recomendar; no edita el expected de un case durante una evaluación ni promueve una capacidad. Ver [`capability-lifecycle.md`](capability-lifecycle.md) para los límites del Foundry.


## Definition of Done

Una tarea está lista para cierre cuando:

- entrega el resultado acordado o explica con evidencia por qué no pudo obtenerse;
- las afirmaciones importantes apuntan a fuentes, cálculos, consultas, runs o criterios relevantes;
- separa hechos observados, verificaciones deterministas, inferencias, supuestos y recomendaciones;
- documenta limitaciones, supuestos materiales y verificaciones pendientes;
- los checks definidos para la tarea se ejecutaron y sus resultados están representados con honestidad;
- la salida cumple el formato específico acordado, con checks de formato y contenido separados;
- actualiza aceptación/owner/siguiente paso y el estado persistente cuando corresponde;
- no se realizaron acciones externas o de producción fuera del alcance autorizado.

Para una UI, tratar como áreas distintas la validación funcional, la evaluación de uso, accesibilidad, handoff Figma-code y visual QA. La disponibilidad y límites de `ui-planning`, `figma-handoff` y `visual-qa` están en [`../playbooks/product-ui-and-prototyping.md`](../playbooks/product-ui-and-prototyping.md). Un reporte visual no prueba usabilidad ni corrección de negocio.


## Paradas y escalamiento

Detener, reducir alcance o pedir una decisión humana ante:

- fuente, cuenta, datos o acción sin autorización confirmada;
- definiciones incompatibles de KPI, población, target o unidad;
- datos insuficientes o discrepancia crítica que invalida el resultado;
- ausencia de un owner necesario para aceptar definición o acción;
- limitación de herramienta/runtime que impide hacer la verificación requerida;
- acciones irreversibles, distribución externa o cambios de producción fuera del mandato.

Comunicar qué se sabe, qué falta, el impacto de la brecha y opciones seguras para continuar. No rellenar silenciosamente la brecha con un supuesto.

