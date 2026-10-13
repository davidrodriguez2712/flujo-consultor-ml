# Foundry — verificación local del transporte nativo

## Estado

Adaptación aprobada implementada y verificada localmente. Suite completa: **214 pruebas pasadas, cero fallos, errores o skips** (12.79 s). Claude Code real 2.1.296 y proveedor HTTPS sustituido por respuestas SSE deterministas. **Cero llamadas pagadas, US$0 de API**. No se cargó `.env` ni una credencial real.

Esta evidencia acredita funcionamiento de infraestructura. La eficacia de `detect-leakage` permanece **NOT_EVALUATED**; tampoco constituye una revisión independiente ni autoriza promoción en Foundry.

## Cambios

- `runtime_budget.py`: opt-in de herramientas locales Read/Write/Bash/Skill para Haiku 5.5. Los defaults anteriores siguen rechazando estas herramientas. Cada solicitud reserva presupuesto; el modo opt-in valida toda la respuesta antes de entregar instrucciones de herramientas al CLI.
- `foundry_native_transport.py`: workspace nuevo con expediente público, plugin local solo en treatment, workflow común opcional congelado, configdir aislado, MCP vacío y permisos explícitos. Multipaso con máximo ocho solicitudes por invocación, límite global y `end_turn` terminal. Fallos detienen nuevas solicitudes.
- `foundry_input_facts.py`: utility fija de stdlib para hashes, tamaño, columnas y conteos de CSV. No evalúa leakage ni ejecuta los pipelines suministrados. Los timestamps se inspeccionan en los inputs; la utility no inventa disponibilidad temporal.
- Se verifica integridad de inputs, skill, metadata del plugin y utility. Escritura limitada a un reporte nuevo. La confirmación nativa de Skill se registra separada del intento solicitado; no basta descubrir el comando.

## Evidencia comprobada

Baseline: lectura real de CSV, escritura del reporte y finalización en tres solicitudes simuladas. Treatment: Skill nativa con snapshot idéntico, utility readonly, reporte y finalización en cuatro solicitudes simuladas. El contenido de la skill y los hechos producidos por la utility llegaron al contexto del CLI.

Los controles negativos bloquearon antes de entregar `tool_use`: lectura de expected fuera del workspace, escritura sobre inputs y comando Bash arbitrario. También se comprobaron symlinks, inputs alterados/eliminados, reporte previo o segunda escritura, herramientas remotas, modelo distinto, usage desconocido y fallo de transporte sin nueva solicitud al proveedor. Las reservas permanecen retenidas cuando no se conoce el uso.

Estos controles son específicos del runner y de los canales comprobados. No acreditan un sandbox del sistema operativo ni una imposibilidad universal de escape. La API puede consumir presupuesto en una respuesta posteriormente rechazada; por eso se conserva su ledger/reserva.

## Desarrollo y conservación

Se observaron fallos iniciales y luego correcciones verificadas: opción opt-in ausente; SSE simulado con deltas incorrectos; reglas de permisos de escritura incompatibles con el CLI; fallo de transporte sin cierre; modelo distinto sin flag persistente; utility/plugin fuera del inventario de hashes e input eliminado sin respuesta de rechazo. Las pruebas nuevas fallaron antes de las correcciones y pasaron después. La ejecución inicial colgada se interrumpió localmente; no hubo proveedor real.

Se conservan XML de la suite, resumen, snapshots de código/pruebas y logs/reportes de los cinco probes nativos (dos positivos y tres negativos), dentro de `evaluations/foundry/2026-10-10-detect-leakage-01/transport-implementation-01/`. Los importes mostrados por el CLI en estos logs provienen de tokens simulados y **no son facturación real**. Las rutas temporales identifican la ejecución original.

Los **620 archivos históricos** incluidos en los manifests comprobados mantienen sus hashes. Paquete original, expected y Foundry canónico intactos. No se actualizaron wheels ni snapshots de pilotos.

## Pendientes

1. Preparar y congelar el coordinador/configuración del estudio: mismo workflow en ambas ramas, smoke y tres pares, límites globales y por sesión, orden y ledger persistente. El transporte ya puede recibir ese workflow; todavía no se ejecutó un estudio completo con él.
2. Aceptación humana de cases, expected y regla de evaluación; reviewer distinto del autor pendiente. Una revisión del autor se identificará como tal.
3. Autorización vinculada al nuevo manifest para gasto de API. US$0.10 sigue siendo propuesta; esta aprobación de implementación local no lo autorizó.
4. Ejecutar y calificar pares sin reparar outputs, conservar incompletos y decidir con la evidencia si corresponde avanzar en el ciclo Foundry.

La propuesta histórica de configuración conserva su estado original como evidencia de aquella preparación; este informe registra el avance posterior.

Referencia utilizada para configurar rutas y escritura: [permisos de Claude Code](https://code.claude.com/docs/en/permissions). El funcionamiento concreto se comprobó con el CLI instalado.
