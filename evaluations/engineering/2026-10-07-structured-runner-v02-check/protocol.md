# Check técnico del runner 0.2.0

Autorizado por el usuario. Dos invocaciones Claude CLI: baseline y treatment, sin reintentos del runner. Se reutiliza el case E de la ronda 02; no constituye una nueva evaluación de eficacia ni modifica aquella ronda. Modelo solicitado: claude-sonnet-5-5, effort medium. Schema común 0.1.0 draft-07 sin expected. Expected permanece fuera del payload y del runner.

Criterios previos: runtime_success, schema_conformant y model_matches deben ser verdaderos. schema_conformant incluye validación estricta Pydantic, textos no vacíos, Unicode válido e IDs únicos, además del schema nativo. Comprobar externamente IDs E1/E2, seis campos, dos decisiones y gate NEEDS_REVIEW. La revisión de razones y preguntas se registra aparte. El runner no corrige outputs ni sustituye structured_output con result. Un fallo se conserva; no genera automáticamente otro call.

Registrar raw exacto, request, objeto nativo, metadata, checker y hashes. Número de invocaciones CLI no equivale a número de requests internos. Coste reportado por CLI, no factura. Congelación local: no acredita cronología externamente. La utilidad se ejecuta desde el checkout, no es un comando instalado de acos.
