# Revisión independiente del contrato nativo

Fecha: 2026-10-12. Comparación: snapshot `2026-10-11-detect-leakage-v02/closure-snapshot-01` frente a scripts actuales `foundry_native_transport.py`, `foundry_study.py` y tres archivos de tests del contrato/transporte/coordinador. No existe repositorio Git; no se inicializó. Se leyeron `superpowers:requesting-code-review` y su template. Único artefacto escrito por esta revisión: este documento.

## Fortalezas

- `runtime_success`, `contract_success` y `execution_success` conservan significados distintos. El coordinador detiene el schedule si falta o falla el contrato, cierra el presupuesto en `finally` y deja `effectiveness: NOT_REVIEWED`.
- El checker lee el reporte sin repararlo; exige metadata conocida coincidente, cobertura exacta de paths/hashes, rechaza duplicados YAML e inventarios duplicados y cuenta whitespace de todo el archivo y respuesta final por separado.
- El contexto se genera desde la condición y snapshot instalado, forma parte del inventario protegido de `ToolPolicy` y no introduce conclusiones de auditoría. El prompt y sus hashes quedan guardados, junto al reporte original y su digest.
- Hay pruebas de comportamiento de CLI real con proveedor sustituido, tanto para contrato inválido como válido, además de pruebas de coordinación y límites negativos. Un PASS mecánico mantiene `semantic_review: REQUIRED`.

## Críticos

Ninguno identificado en los cambios revisados.

## Importantes

1. **Encabezados dentro de bloques de código cuentan como secciones.** `scripts/evaluations/foundry_native_transport.py:96`. La regex procesa el cuerpo Markdown sin distinguir fences: con frontmatter válido, envolver todas las cinco secciones en un único bloque ` ```markdown ` produce `success: true`, `errors: []`. El reporte renderizado no tiene ninguna de esas secciones; solo muestra código. Esto permite continuar el schedule y restaurar presupuesto tras un incumplimiento estructural verificable mecánicamente. Corregir el conteo para considerar únicamente encabezados Markdown reales fuera de fences/comentarios y probar fences de backticks y tildes, así como ejemplos duplicados que no deban contar. El repro usó la fixture existente, modificó solo un reporte temporal y no hizo llamadas.

## Menores

1. **Fecha YAML inválida se diagnostica como duplicado.** `scripts/evaluations/foundry_native_transport.py:60`. `fecha: 2026-99-99` causa un `ValueError` del constructor timestamp de PyYAML, capturado como `frontmatter:duplicate`, aunque no hay claves duplicadas. Permanece cerrado, pero contamina la explicación del fallo. Usar excepción específica para duplicados y distinguir metadata inválida.
2. **Contexto JSON malformado escapa del checker.** `scripts/evaluations/foundry_native_transport.py:68` y `:99`. Un contexto con `{bad json` lanza `JSONDecodeError` en vez de devolver el resultado mecánico fallido. El contexto se genera localmente y está protegido, y el `finally` del coordinador cierra presupuesto ante excepción; por eso no se presenta como bypass de seguridad de la ejecución normal. Capturar el error de JSON devolvería evidencia consistente ante corrupción local y permitiría persistir `report-contract.json`.

## Verificación y límites

Comando local: `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_foundry_report_contract.py tests/test_foundry_study.py tests/test_foundry_native_transport.py`.

Resultado de esta ejecución: **39 passed, 14 failed**. Los 14 fallos ocurren al abrir el socket localhost del proxy (`PermissionError: Operation not permitted`), por restricciones del sandbox; no corroboran un defecto funcional del transporte. No se escalaron permisos ni se realizaron llamadas al proveedor. El dato de 253 PASS del coordinador es antecedente proporcionado, no resultado reproducido por esta revisión. La prueba positiva CLI añadida durante la revisión se leyó; su ejecución aquí también quedó bloqueada por el socket. Los repros del checker se ejecutaron sin sockets y confirmaron los tres hallazgos.

No se modificaron implementación, tests, cases, expected, outputs históricos ni skill canónica. No se auditó íntegramente el inventario histórico: la revisión del diff no sustituye sus manifests de integridad.

## Comportamientos considerados y descartados

- Veracidad de hallazgos, suficiencia de evidencia, legitimidad de `estado` y fecha real de ejecución: requieren revisor humano/agente semántico; no deben inferirse de PASS mecánico.
- Aprobación de gates, promoción de skill o eficacia general: fuera del contrato y de esta revisión; el código conserva esos límites.
- Reejecución de paquetes históricos con scripts raíz nuevos: fuera de alcance; los contratos nuevos deben congelarse en futuras configuraciones y no reinterpretar outputs históricos.
- Parser Markdown general, estilos alternativos de títulos y campos adicionales de metadata: no se exige soporte universal; sí debe impedirse el falso positivo estructural demostrado.
- Persistencia tras muerte abrupta del proceso y ataques concurrentes externos al workspace: limitaciones preexistentes; no introducidas por este diff.

## Veredicto

**Requiere corrección antes de considerar completo el contrato:** resolver el falso positivo de secciones en fences y añadir su regresión. La separación runtime/mecánica/semántica y la parada normal ante contrato fallido están bien planteadas. Esta revisión no autoriza ejecución pagada ni certifica hallazgos semánticos.
