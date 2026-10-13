# Ejecución Foundry 01

## Estado

Configuración preparada; NO AUTORIZADA para API. L01 leakage posterior al scoring; L02 historial temporal válido de clientes conocidos; L03 disponibilidad desconocida. Datos sintéticos, una repetición por rama: no generalización. Expected privado conservado antes de outputs, nunca copiado al workspace.

## Revisión solicitada a David

Revisar PROTOCOL.md y reviewer/L01–L03/expected.md. Confirmar aceptación de casos/regla y actuar como reviewer distinto del autor si se desea revisión independiente. Regla: mejora conjunta en al menos dos casos, ninguna regresión ni falso positivo crítico; empate/efecto techo no acredita mejora. Evaluación humana con evidencia, no búsqueda de frases.

## Verificar sin credenciales

Desde raíz del workspace:

```sh
.venv/bin/python evaluations/foundry/2026-10-10-detect-leakage-01/execution-config-01/snapshots/scripts/evaluations/foundry_study.py --package evaluations/foundry/2026-10-10-detect-leakage-01/execution-config-01 --verify-only
```

El manifest incluye todos los archivos del paquete excepto el propio manifest; snapshots no se actualizan durante la comparación. El comando verifica hashes sin cargar .env ni acceder a API. Los paths temporales de logs identifican la ejecución original. No editar código congelado: cambios requieren nueva configuración y manifest.

## Autorización posterior

Solo después de aprobación explícita, registrar approval.json FUERA de este paquete: status APPROVED, execution_manifest_sha256 exacto, total_budget_usd hasta 0.10 y package_accepted true. El fichero registra la decisión humana, no la sustituye. No reutilizar autorizaciones de otros estudios.

## Ejecutar después de autorización

Usar el mismo comando congelado con --approval RUTA_APROBACION --output RUTA_NUEVA en lugar de --verify-only. ANTHROPIC_API_KEY debe estar en el entorno autorizado; no se carga .env automáticamente. Versión CLI exacta, settings vacíos, MCP vacío, sin retries. Proxy reserva cada request y puede parar por presupuesto antes de completar los pares. No reanudar ni repetir sin nueva autorización. Solo siete invocaciones/56 solicitudes máximas, cada sesión ocho y 240 segundos.

## Revisión posterior

Conservar stdout, stderr, reportes y ledger originales. runtime_success no significa contenido correcto. Registrar por rama formato/persistencia, contenido, correctitud, cobertura, fundamentación, accionabilidad, coste y tiempo. Verificar hashes/fecha y eventos Skill reales. Pares incompletos se conservan y no cuentan como señal favorable del plan entero. Foundry no se promueve automáticamente: decisión posterior con reviewer identificado y limitaciones.

## Límites

Utility produce hashes/conteos, no ejecuta pipeline ni compara fechas por cuenta propia. restricted no equivale a sandbox OS; controles de herramientas probados específicamente. Uso desconocido mantiene reserva. Los US$0.10 son límite de trabajo del proxy, no garantía contractual del proveedor ni cobertura de GitHub Actions. No se han hecho llamadas pagadas en esta preparación.
