# Ejecución propuesta de la evaluación

## Estado

Configuración preparada; gasto sin autorizar. Cero llamadas reales. Un smoke técnico y doce invocaciones, una repetición por combinación, con Claude Code 2.1.295 y `claude-haiku-5-5`. No habilitar fallback de modelos.

## Antes de ejecutar

1. Obtener autorización explícita del usuario para hasta **US$0.20 total**, incluyendo smoke y benchmark. Registrar su respuesta literal en un archivo nuevo `budget-approval.json`, fuera del manifest: `status: APPROVED`, `total_budget_usd`, `execution_manifest_sha256` del manifest de esta carpeta. El presupuesto antiguo de Windows no aplica.
2. Comprobar el hash de ese manifest y cada archivo incluido. Comprobar los 48 archivos del manifest de preparación, su hash aceptado y la aprobación humana de revisión. Comprobar que los scripts de trabajo coinciden con sus snapshots antes de importarlos. No modificar ninguno de los dos freezes.
3. Comprobar `claude --version`. Un cambio exige revisar configuración; no usar silenciosamente otra versión/modelo.
4. Llamar a `require_approval` del transporte antes de consultar credenciales o crear `Proxy`. La clave Anthropic debe proporcionarse al proceso mediante un mecanismo local seguro. Nunca incluirla en argv, evidencia ni logs. No asumir que el secret de GitHub está disponible en esta laptop. Si no hay clave local, detenerse y pedir únicamente el mecanismo para proporcionarla, no su valor por chat.

## Transporte

Las funciones se encuentran en `scripts/evaluations/workflow_native_transport.py` y el control en `scripts/ci/runtime_budget.py`; son utilidades de evaluación, no comandos nuevos de ACOS.

El coordinador usa una sola instancia `Proxy('claude', key, approved_limit, model='claude-haiku-5-5', max_requests=13)` para smoke y benchmark. Su ledger es compartido por toda la ronda; nunca reiniciarlo para obtener presupuesto adicional.

Para cada ejecución llama a `invoke(payload_text, new_output_directory, proxy, native_cli_path)`. Cada directorio debe ser nuevo. No llamar a `invoke` después de un fallo de transporte ni después de 13 requests. Cada llamada permite un único request adicional; los intentos de continuación/retry se bloquean antes del proveedor.

El modelo solo recibe el payload y el system prompt genérico registrado, en un proceso nuevo y cwd temporal vacío. `--bare` usa API key explícita; la clave real reside únicamente en el proxy y el CLI recibe un placeholder local. `--safe-mode`, herramientas vacías y MCP vacío deshabilitan personalizaciones. Sin sesión persistente, Chrome, skills ni fuentes de settings del usuario/proyecto.

No se ha creado un sandbox de sistema operativo. Las políticas administradas del CLI todavía pueden aplicar. Estos controles se han comprobado con subprocess/proveedores simulados; el smoke real debe confirmar compatibilidad y comportamiento observable. No afirmar aislamiento nativo verificado antes de ese smoke.

## Orden y parada

1. Ejecutar `smoke-payload.txt`, separado de los seis cases. Exigir runtime exitoso, un request, usage conocido, modelo exacto y JSON del contrato. El smoke no puntúa eficacia.
2. Si pasa, ejecutar las doce entradas de `config.json: order`, sin expected, case-index, resultados previos ni archivos de esta carpeta en el prompt. No modificar payloads ni corregir respuestas.
3. Tras cada invocación preservar payload, stdout, stderr, result textual y metadata. Guardar copia del ledger de presupuesto y rejections fuera de los freezes, incluso ante fallo.
4. Parar si runtime falla, se corta por tokens/timeout, falta usage, cambia modelo, se excede reserva, hay múltiples requests o falla integridad. Conservar pares incompletos; no imputar respuestas ni efectuar reintentos.
5. Un error JSON, referencias inexistentes o respuesta incorrecta del benchmark se registra como resultado de evaluación; no se repara ni provoca un retry. Un smoke con esos errores detiene la ronda.

## Presupuesto

El proxy reserva antes de cada solicitud. Para 5.5 aplica reserva conservadora de bytes UTF-8 + 16.384, cache write de 5 minutos del tier largo y 2.048 tokens de salida a tarifa del tier largo. Registra por separado reserva, usage y estimación. Si usage no llega, conserva la reserva completa. Si el coste observado supera la reserva, bloquea solicitudes posteriores.

Es una cota heurística de tokenización y control local, no una garantía de factura final. El total propuesto no incluye impuestos ni un proveedor adicional. No usar herramientas remotas, Priority Tier, inference geography con recargo ni otras llamadas fuera del proxy.

Tarifas verificadas el 9 de octubre de 2026: [pricing oficial](https://platform.claude.com/docs/en/about-claude/pricing). Thinking adaptativo consume parte del límite de salida; effort low no garantiza ausencia de thinking: [migration guide](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide).

## Evaluación posterior

Ejecutar el checker local después de obtener las respuestas; el modelo no recibe expected. El checker informa formato, estado y existencia de referencias. `semantic_review: NOT_RUN` y `overall_content_pass: null` permanecen hasta revisar soporte de findings, acciones obligatorias/prohibidas, falsos bloqueos y autoridad según los expected congelados.

Revisión semántica con códigos ciegos de condición cuando sea posible; registrar quién revisa y cualquier conocimiento previo de expected/condición. La revisión del mismo autor no es independiente. Publicar resultados por case/condición, errores de formato/transporte, costes y limitaciones. Aplicar la regla exploratoria ya fijada en el protocolo, sin cambiar umbrales después de ver resultados ni promover capacidades del Foundry.
