# detect-leakage — intento real 01 detenido en smoke

## Resultado

El usuario aceptó el paquete/regla y autorizó hasta US$0.10 total para el manifest `64a52f85b39eedcff77a7ca47f17c5b8664791db48aea0063971e3915480ede0`. Aprobación registrada fuera del paquete congelado, en `authorization-01/approval.json`.

Se verificaron hashes, Claude Code 2.1.296 y tarifas antes de ejecutar. Se cargó únicamente ANTHROPIC_API_KEY del .env autorizado, sin imprimir, copiar ni hash de la credencial. El smoke produjo **una solicitud real a Anthropic**, HTTP200, uso conocido y `tool_use`. El guard rechazó un comando Bash fuera de la whitelist exacta antes de entregar herramientas al CLI. No se creó reporte.

El coordinador se detuvo: **cero casos L01–L03, cero pares evaluados, eficacia NOT_EVALUATED**. No segunda solicitud al proveedor ni retry pagado. El CLI intentó otra solicitud al proxy, bloqueada localmente; eso se conserva como rechazo, no llamada facturada.

## Consumo

Uso reportado: input fresco2, cache creation5m3903, output402 (incluye24 thinking). Coste estimado **US$0.000689075**: `(2×0.10 + 3903×0.125 + 402×0.50)/1_000_000`. Reserva inicial US$0.037606875, liquidada con uso conocido. Son consumo estimado según tarifas y respuesta API, no conciliación de factura.

Las tarifas coinciden con el snapshot y con la [documentación oficial de Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), consultada el 2026-10-11. El CLI imprime coste cero porque no recibió la respuesta rechazada; ese cero no representa el gasto real. Quedan US$0.099310925 del límite aprobado, pero no autorizan un nuevo intento de este estudio: el plan prohíbe retries y una corrección cambiaría el manifest.

## Diagnóstico y límites

Hecho comprobado: respuesta de proveedor válida seguida de `tool_guard_error: Comando no permitido`. El CLI traduce el 403 del proxy como `authentication_failed`; no hay evidencia de clave inválida ni HTTP401 del proveedor.

Brecha identificada por inspección: prompt/case solicitan una utility fija pero no explican su comando exacto. Las pruebas mock suministraban ese comando directamente, por lo que verificaban ejecución/aislamiento, no que el modelo lo seleccionase. La utility se ejecutó después por el autor, de forma local, y devolvió una fila CSV y hashes; este check no se atribuye al agente ni convierte el smoke en PASS.

Hipótesis: el modelo eligió otro comando por falta de instrucciones operativas suficientes. El proxy congelado no conserva el input de herramienta rechazado ni la respuesta cruda bloqueada, de modo que el comando concreto y el motivo de elección no pueden reconstruirse. No inventar que fue `ls`, `pwd`, otra ruta de Python ni un fallo de quoting. No relajar permisos para hacer pasar el smoke.

## Conservación

Run original, stdout/stderr, metadata, ledger, inputs y revisión congelados en `runs/round-01/run-manifest-01.json`: 13 archivos, SHA256 `d1c3bcb4e73ee647d29ab301ff5a51adbb60b09dff85c8860395b04917f543b0`. Configuración29archivos intacta. Foundry canónico y madurez sin cambios. Revisión realizada por autor, no independiente.

## Siguiente diseño acotado propuesto

1. Presentar al modelo el comando exacto de la utility y los límites Read/Write/Bash/Skill en una instrucción operativa común a ambas ramas. No añadir expected ni pistas sobre leakage.
2. Conservar en evidencia local el nombre e input de la herramienta rechazada, con límites y redacción de secretos antes de persistencia; no registrar headers/credenciales ni entregar comandos rechazados al CLI.
3. Verificar localmente la nueva instrucción y el registro de rechazo, junto con la suite de controles existente. No usar mocks como eficacia ni garantía de selección futura del modelo.
4. Congelar una configuración nueva y solicitar autorización vinculada antes de otro smoke real. No modificar ni reanudar round01; mantener Foundry/expected y restricciones originales.

La skill `superpowers:brainstorming` exige aprobar este diseño acotado antes de cambiar comportamiento del runner. La autorización del estudio01 ya ejecutado no aprueba gasto ni ejecución de una configuración nueva.
