# Seguimiento de revisión independiente

Fecha: 2026-10-12. Se conserva `REVIEW.md` como evidencia de los hallazgos iniciales. Se revisaron las correcciones actuales en `foundry_native_transport.py`, sus regresiones en `test_foundry_report_contract.py` y la prueba positiva CLI en `test_foundry_native_transport.py`.

## Resolución de hallazgos

- **Importante, secciones dentro de fences: resuelto.** `report_headings` omite bloques de backticks/tildes y comentarios HTML, conserva el estado de cada fence y solo reconoce su cierre con el mismo carácter y longitud suficiente. Se reprodujo el caso inicial con backticks, tildes y cuatro backticks: los cinco errores `section:*` aparecen y `success` es falso. Un reporte válido sigue pasando. La prueba de ejemplo dentro de código garantiza que un encabezado de ejemplo no se cuente como duplicado. No se transforma ni reescribe el reporte.
- **Menor, fecha inválida diagnosticada como duplicado: resuelto.** `DuplicateReportKey` identifica duplicados; los errores del constructor YAML, incluido `2026-99-99`, generan `frontmatter:invalid`. La regresión distingue ambos diagnósticos.
- **Menor, contexto JSON inválido: resuelto.** La captura externa de `ValueError` cubre `JSONDecodeError`, devuelve `contract:unreadable` y conserva el reporte. El repro inicial ya no escapa del checker.
- **Defensa adicional de procedencia: correcta en la ruta normal.** El checker verifica fuentes y sus ancestros antes de sus digest, rechaza symlinks con `inputs:unsafe` y exige que exista `case.md`. La prueba observa los paths realmente enviados a `digest` y comprueba que no se leen los bytes del destino externo. `invoke` ya utiliza un root resuelto; el rechazo de ancestros symlink del helper es deliberadamente conservador.

## Verificación propia

`.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_foundry_report_contract.py tests/test_foundry_study.py`: **39 passed, 0 failed**, 0,10 s. Repros temporales independientes del checker confirmaron fences, fecha inválida, contexto inválido y persistencia de la aceptación de un reporte válido. También se comprobó directamente que un cierre de tres backticks no termina un fence abierto con cuatro: solo el encabezado posterior al cierre válido se reconoce.

La prueba positiva CLI se revisó por lectura: comprueba runtime/contrato/ejecución verdaderos, presupuesto restaurado a ocho, reporte sin alteración y `semantic_review: REQUIRED`. Su PASS con permisos localhost y el resultado de la suite completa corresponden a la verificación del coordinador; no se presentan como ejecución propia de este seguimiento. No se hizo otra ejecución de sockets bajo el sandbox que ya los rechazó. No hubo llamadas a APIs ni lectura de credenciales.

## Hallazgos pendientes

Críticos: ninguno. Importantes: ninguno en los cambios corregidos y el contrato ATX delimitado. Menores: ninguno de los tres hallazgos iniciales permanece abierto.

## Comportamientos considerados y descartados

- Parser universal Markdown/HTML, títulos Setext y sintaxis anidada arbitraria: fuera del contrato ATX declarado; las correcciones cubren fences y comentarios que motivaron el hallazgo concreto. No se afirma conformidad universal con todos los renderizadores.
- Veracidad de hallazgos, adecuación del estado y fecha real, aprobación de gates y eficacia de la skill: requieren revisión humana/agente semántica; no se deducen de estos checks.
- Carreras con actores externos que sustituyen archivos entre validación y lectura: fuera del modelo de ejecución local autorizado de esta revisión; no se afirma protección atómica contra mutaciones externas concurrentes.
- Cambiar criterios de resultados históricos o actualizar snapshots anteriores: fuera del alcance, reservado a futuras configuraciones.

## Veredicto actualizado

**Apto para cerrar esta implementación del contrato mecánico**, con los tres hallazgos iniciales corregidos y regresiones propias verdes. El cierre del contrato no certifica hallazgos semánticos ni autoriza ejecución pagada. La evidencia inicial y sus limitaciones se conservan en `REVIEW.md`.
