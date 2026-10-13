# Foundry — coordinador y configuración congelados

## Estado

Coordinador preparado y configuración de 29 archivos congelada. Verificación sin credenciales: PASS_FROZEN_CONFIG. Suite completa: **223 pruebas pasadas**, cero fallos (12.61 s). **API US$0, ninguna llamada pagada**. Eficacia NOT_EVALUATED; Foundry canónico intacto.

## Coordinación

Sigue el diseño acordado: smoke técnico, L01 baseline/treatment, L02 treatment/baseline y L03 baseline/treatment. Mismo workflow congelado y expediente público por caso. Skill experimental 0.1.0 solo en treatment. Expected privado no se entrega al transporte. Máximo siete invocaciones, ocho requests por sesión, 56 globales, cap8192 y timeout240s. Presupuesto nuevo propuesto hasta US$0.10; no autorizado.

Antes de leer credenciales comprueba hashes, autorización vinculada al manifest, aceptación humana del paquete, versión exacta Claude Code2.1.296 y output nuevo. No carga .env automáticamente. Guarda ledger por sesión y al salir, detiene tras fallo y conserva outputs sin repararlos. No permite reanudar ni sobrescribir. No ofrece persistencia duradera ante terminación abrupta del proceso/sistema durante un request; el proxy mantiene reserva en memoria y el coordinador la guarda al salir normalmente o por excepción.

## Verificación

Nueve pruebas nuevas comprueban rechazo de autorizaciones incompletas/excesivas, aceptación ligada a hash, orden, workflow compartido, skill solo en treatment, parada, conservación del ledger ante excepción y rechazo de output existente. Son pruebas de coordinación con transporte simulado; las pruebas previas del transporte con Claude real/proveedor simulado también pasaron en la suite completa. Ninguna mide eficacia semántica.

Paquetes históricos Foundry de 27, 12 y 89 archivos siguen íntegros. El nuevo paquete copia cases, expected, protocolo, workflow, skill y fuentes/pruebas; no modifica sus originales. Manifest SHA256: `64a52f85b39eedcff77a7ca47f17c5b8664791db48aea0063971e3915480ede0`.

## Revisión y autorización pendientes

Revisar `execution-config-01/RUNBOOK.md`, `PROTOCOL.md` y `reviewer/L01–L03/expected.md`: escenarios sintéticos de leakage posterior, split temporal válido y disponibilidad desconocida. Regla favorable: mejora conjunta en al menos dos casos, ninguna regresión ni nuevo falso positivo crítico. Una repetición por rama no acredita estabilidad/generalización. El autor conoce los expected; revisión actual no independiente.

David puede actuar como reviewer distinto del autor; asignación y revisión de resultados pendientes. Para ejecutar falta aceptación explícita del paquete/regla y autorización hasta US$0.10 para el manifest indicado. La autorización de preparación no equivale a gasto. Si el presupuesto no alcanza, conservar pares incompletos; no hacer retries ni gastar saldo de otros estudios. No promover automáticamente Foundry.

## Archivos

- Coordinador: scripts/evaluations/foundry_study.py.
- Paquete: evaluations/foundry/2026-10-10-detect-leakage-01/execution-config-01/.
- Evidencia de pruebas: evaluations/foundry/2026-10-10-detect-leakage-01/coordinator-verification-01/.
