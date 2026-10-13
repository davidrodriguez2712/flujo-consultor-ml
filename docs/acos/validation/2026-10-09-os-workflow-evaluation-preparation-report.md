# Evaluación menos guiada de pautas — preparación

Estado: PREPARED_FOR_REVIEW. Preparación autorizada, ejecución no autorizada. Modelo/runtime/configuración/budget aún sin fijar. Cero llamadas de modelos, costo API US$0.

## Paquete concreto

[Protocolo](../../../evaluations/os-workflow/2026-10-09-less-guided-01/protocol.md) · [README](../../../evaluations/os-workflow/2026-10-09-less-guided-01/README.md) · [Checks locales](../../../evaluations/os-workflow/2026-10-09-less-guided-01/preparation-checks.json).

| Caso | Tipo | Pregunta que discrimina |
|---|---|---|
| E01 | Freeze, defecto | ¿Detecta que la aprobación anterior apunta al plan vivo que cambió? |
| E02 | Freeze, coherente | ¿Permite actualizar plan vivo cuando la copia aprobada permanece intacta? |
| E03 | Reproducción, defecto | ¿Detecta selección diferente al omitir serialización aunque valores estén dentro de tolerancia? |
| E04 | Reproducción, coherente | ¿Acepta equivalencia semántica con distinto whitespace cuando el contrato lo permite? |
| E05 | Etiquetas, defecto | ¿Detecta cifra de otra población y excluye período incompleto? |
| E06 | Etiquetas, coherente | ¿Conserva un borrador correcto pese a filas posteriores no elegibles? |

Baseline: workflow actual sin las tres secciones nuevas; treatment: mismo workflow con ellas. No es comparación de releases completas. Inputs/contrato iguales. Se prepararon doce payloads, uno por case/condición, sin expected ni protocolo. Casos hipotéticos, sin datos privados.

## Verificación

Comando: `.venv/bin/python evaluations/os-workflow/2026-10-09-less-guided-01/verify_preparation.py`.

PASS: seis cases equilibrados, ensamblado de doce payloads, diferencia exclusiva del suplemento, hashes de fixtures, writer/reader real para el contraejemplo, JSON semánticamente equivalente y 24 órdenes por cada case temporal. Manifest congelado verificado: 48 archivos; SHA-256 del manifest `90544d163b168930e86373699ede98b7f099b54d1b7d7d5ea9487d1c50362e19`. Aprobación/configuración futuras quedan fuera del freeze.

No se ejecutó la suite de producto: no se modificó código del compiler. Estos checks locales verifican la preparación, no puntúan outputs de modelos ni demuestran eficacia. Revisión nativa del mismo autor; aislamiento efectivo del runtime pendiente. La representación ambigua inicial del manifest fue corregida antes del freeze y sin calls.

## Antes de ejecutar

1. Aceptar o corregir el protocolo y los expected concretos.
2. Fijar runtime/modelo, transporte compatible, checker de outputs y configuración de aislamiento.
3. Autorizar presupuesto nuevo y ejecución; conservar request/raw/metadata por intento. Propuesta económica: una réplica por case/condición, doce invocaciones, sin reintentos automáticos.

El author no debe actuar como modelo evaluado en la conversación que conoce expected. Usar contextos frescos y payload-only con herramientas deshabilitadas. Una réplica solo produce señal exploratoria. No creación/promoción de capacidades del Foundry ni publicación externa.
