# Ejecución propuesta — todavía no autorizada

## Antes de llamar al proveedor

1. Verificar manifest de preparación, aprobación concreta contra su hash, este freeze de configuración y snapshots. Usar código revisado, no copiar el coordinador antiguo sin cambios.
2. Registrar una aprobación nueva de gasto contra SHA-256 de execution-manifest-01.json. `require_approval` debe pasar antes de cargar credencial o crear Proxy. Propuesta: US$0.10 adicionales como máximo para smoke y doce invocaciones; ninguna autorización actual de pago. No sumar ni reutilizar presupuestos de Windows/estudio anterior.
3. Verificar CLI/version/flags exactos; cambios requieren revisión registrada. Revalidar pricing si cambia antes de ejecución.
4. Cargar exclusivamente ANTHROPIC_API_KEY desde entorno o parser seguro de `.env`, sin `source`, comandos shell, impresión, hash o copia del secreto. Ejecutar mediante proxy con placeholder local para la clave del CLI.
5. Crear directorio de run nuevo, conservar todas las respuestas/intentos. Crear `Proxy('claude', key, limit, model=MODEL, max_requests=13, max_output_tokens=8192)` únicamente después de aprobación. El budget inicial es solo el nuevo estudio; registrar referencia histórica US$0.02065453 separada.

## Smoke y doce invocaciones

- Usar `invoke(payload, target_nuevo, proxy, cli, system_prompt=TRANSFER_SYSTEM)` explícitamente en smoke y TODAS las celdas. Comprobar que config system_prompt coincide con constante revisada. No modificar prompts por condición o resultado.
- El envelope del CLI sigue JSON; `result.txt` permanece texto sin reparar. Smoke Markdown con expected local `{status: READY, format: markdown}` y artifacts vacíos; chequeo estructural, no eficacia. No enviar expected/protocolo al CLI. Debe tener runtime_success, un request con usage conocido y provider_stop_reason=end_turn; luego formato/status/rutas conformes.
- Seguir config.order con fresh process/cwd y sin herramientas. Solo un payload público por invoke. Coordinator/reviewer local puede leer expected después de respuesta; el child evaluado no lo recibe.
- Después de cada request persistir raw/metadata/ledger antes de continuar. Exigir runtime_success y end_turn. Si proveedor/runtime/presupuesto falla, detener sin retries, conservar consumo y declarar pares incompletos.
- Aplicar checker al raw local después de cada respuesta. Fallo de formato o contenido de benchmark se conserva y puntúa; no lo reemplaza otro call ni fuerza parada de infraestructura.

## Cierre

Persistir estado, usage/costo por request, rejections y orden efectivo. Costos desconocidos son null con motivo; retener reserva y detener. Verificar integridad previa y que no se persistió el valor secreto. Congelar el run antes de atribuir resultados. Revisión semántica con expected congelados, citas y fuente; reportar formato/content/alcance por separado y regla exploratoria, sin Foundry/promociones. No afirmar eficacia del compiler/templates/manual ni independencia. El límite de reserva del proxy no garantiza factura final ni completar todos los casos si se consume el máximo.
