# Configuración nueva — pago no autorizado

## Preflight y autoridad

1. Revisar paquete/expected/rúbrica y configurar aprobación del usuario contra manifest de preparación, fuera del freeze. Revisión autor no sustituye aceptación humana.
2. Autorizar hastaUS$0.10adicionales contra SHA256 de execution-manifest-01.json; require_approval antes de credencial/proxy. No presupuestos anteriores. Guardar ambos registros separados de los manifests.
3. Verificar todos los archivos listados de ambos manifests y snapshots contra código vigente; no recorrer pycache como código aprobado. CLI/version/flags/modelo exactos. Si cambian, detener/revisar antes de paidcall.
4. Cargar solo ANTHROPIC_API_KEY mediante entorno/parser seguro de.env, sin source, imprimir, copiar ni hash de secreto. Proxy local usa clave real, CLI placeholder.

## Ejecución exactamente delimitada

Validar order=8celdas únicas D01–D04×baseline/treatment con orden fijado. Una única invocaciónsmoke más esas ocho, ningún retry. Antes de CADA invoke verificar len(proxy.budget.entries)<9 y que celda pertenece a schedule. Proxy inicialmax_requests9; invoke establece límite dinámico de un request adicional. Helper genérico tiene ceiling13, por eso el coordinador debe aplicar schedule/guard9; eso no autoriza solicitudes10–13. No usar callback recursivo ni copiar order antiguo.

Usar `Proxy('claude', key, limit, model=MODEL, max_requests=9, max_output_tokens=8192)` e `invoke(payload, destino_nuevo, proxy, cli, system_prompt=TRANSFER_SYSTEM)` igual en todas celdas. Proceso/cwdfresh, sin herramientas/skills/MCP/settings/sesión. Nada de protocolo/expected/reviewer dentro de input ni cwd del child.

Smoke Markdown: expectedlocal READY/markdown y artifacts vacíos. Exigir runtime_success, un request y usage/end_turn; checker formato/status/rutas conformes. El smoke incluye explicación bajo Estado para verificar compatibilidad con checker0.2.0, no mide eficacia ni usa cases del benchmark.

Cada celda: persistir stdout/stderr/raw/metadata/ledger; exigir runtime_success/unrequest/usage/end_turn. Error infraestructura/presupuesto/integridad detiene sin retries. Checker sobre raw local con expected después de output; no enviarlo a runtime. Error de formato/content se conserva y puntúa, no se reemplaza ni repara. No almacenar secreto.

## Cierre y review

Congelar todos los intentos/costes, validar integridad/hashes y ausencia de secretoexacto sin imprimirlo. Unknownusage=null y retener reserva, detener. Registrar coste históricoUS$0.04153488 separado, no consumir saldo deotroestudio. Revisar contenido por obligación/citas/source, no presencia de keys. D04control sin task; no agregar denominadores6/4. Interpretación según regla congelada; no modificar expected después de output. No Foundry/promociones por control técnico ni eficacia general.
