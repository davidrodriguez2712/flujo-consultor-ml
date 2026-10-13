# Regresión nativa: configuración preparada 02

Fecha: 2026-10-12. Preparación y simulaciones locales; ninguna llamada real al proveedor ni ampliación del presupuesto autorizado.

## Paquete preparado

L01, L02 y L03 en treatment con snapshot exacto de `detect-leakage 0.2.0 experimental`. CLI Claude Code 2.1.296. Expedientes, workflow y expected legacy preservados. Expected permanece privado y no se copia a los workspaces del CLI.

El paquete congela el transporte corregido: prompt/hash y contrato mecánico persistidos, campos exactos, inventario/hashes, secciones, extensión y parada sin reparar outputs. Máximo ocho requests por invocación, sin reintentos pagados automáticos. Tres invocaciones previstas, máximo24requests; límite global del proxy56 preservado.

Se eleva output cap de4096 a8192 por la truncación anterior de L02. Reporte≤500 palabras, final≤80 incluida ruta. Un cap mayor no garantiza completar la respuesta y puede aumentar la reserva; no se han relajado los guards de presupuesto ni de herramientas.

Freeze de23archivos, manifest SHA-256:
`b8ef2799245a463cc3e33be88c25e94b1b26af13072862d9f6c613ac2e0da044`.

`--verify-only` devuelve `PASS_FROZEN_CONFIG` sin consultar credenciales ni proveedor. `approval.json` sigue `NOT_AUTHORIZED` y el verificador de autorización lo rechaza. No es una aprobación de gasto.

## Simulaciones realizadas

Claude real con HTTPS del proveedor sustituido por SSE determinista y clave ficticia. Skill y utility readonly se ejecutan nativamente. Los reportes declaran ser sintéticos; no contienen una resolución del caso ni incorporan expected. Los ledgers de estas simulaciones no son consumo ni factura reales.

| Simulación | Resultado | Requests al proveedor simulado | Requests reales |
|---|---|---:|---:|
| Límite ficticioUS$0.10 | L01–L03 runtime/contratoPASS; secuencia completa, revisión semántica pendiente | 12 | 0 |
| Saldo real reproducidoUS$0.00887352 | Detención en L01 por presupuesto antes de persistir reporte | 2 | 0 |

En la segunda simulación, los dos usages sintéticos comprometenUS$0.000036; quedaUS$0.00883752. La siguiente solicitud tiene una reserva deUS$0.008994625 y se bloquea antes de enviarse. Esto demuestra la parada en esta secuencia observada; no prueba un coste universal o mínimo de cualquier respuesta posible del modelo. El usage real podría diferir ampliamente del sintético.

La primera simulación verifica el runner y el contrato. **No demuestra que el LLM resuelva L01–L03 ni mejora de la skill frente al baseline.** Sigue pendiente una ejecución real y posterior revisión semántica independiente.

## Presupuesto concreto propuesto

El techo del estudio detect-leakage autorizado esUS$0.10. Consumo estimado previoUS$0.09112648; saldoUS$0.00887352. Gasto adicional en esta preparaciónUS$0.

Propongo autorizar **hastaUS$0.05 adicionales**, llevando el techo acumulado a **US$0.15**. Con el saldo existente, el máximo disponible para la nueva secuencia seríaUS$0.05887352. Es un límite de gasto, no una estimación ni obligación de consumirlo, y no garantiza completar todas las invocaciones.

El margen permite intentar las tres regresiones sin debilitar las reservas ni pedir pequeños aumentos ante cada request. El proxy mantendrá la parada ante contrato/runtime/presupuesto fallidos y no hará retries automáticos. La propuesta no autoriza promociones ni otro proveedor o modelo.

Esta ampliación requiere autorización expresa porque excede el techo previo, aunque las rondas y correcciones estén autorizadas de forma autónoma. `BUDGET_PROPOSAL.json` liga la propuesta al manifest. No se ha leído una clave real ni preparado un approval que declare autorización inexistente.

## Integridad y pendientes

Los222archivos congelados del cierre0.2 y los55del control del contrato conservan sus hashes. La skill canónica sigue0.2.0experimental con el mismo hash. No se modifican resultados históricos ni estados de madurez.

Pendiente inmediato: autorización del presupuesto propuesto, ejecución nueva en carpeta nueva y review independiente de reportes contra expected. Después: comparación controlada con casos menos guiados; la regresión treatment-only no demuestra superioridad causal.

Evidencia: `evaluations/foundry/2026-10-12-native-regression-preparation-02/`, incluyendo paquete, approval rechazado, script experimental de simulación, trazas, ledgers sintéticos, summary, checks, propuesta de presupuesto y manifest de cierre.
