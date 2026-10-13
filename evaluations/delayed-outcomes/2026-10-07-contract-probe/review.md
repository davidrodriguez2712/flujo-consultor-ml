# Review exploratoria — contrato temporal

Fecha: 2026-10-07. Reviewer: asistente que preparó el protocolo, por tanto no independiente. No es evaluación canónica del Foundry.

## Resultado

Ocho ejecuciones válidas: cuatro casos y dos condiciones. Baseline recibió las pautas design-validation 0.1.0 como contenido; treatment recibió exactamente lo mismo más temporal-contract-v0.1.md. No hubo invocación nativa de skills ni herramientas. Ambas condiciones acertaron las nueve decisiones de elegibilidad: no se observó mejora de esa decisión con el suplemento.

| Caso | Decisión principal | Baseline | Treatment |
|---|---|---|---|
| A — Label posterior al cutoff | Incluir A1/A3, excluir A2 aunque la extracción futura traiga 0 | 3/3 correctas | 3/3 correctas |
| B — Igualdad exacta | Incluir B1 por <=; excluir B2 disponible un segundo después | 2/2 correctas | 2/2 correctas |
| C — Pendientes | Excluir C1/C2 sin convertir null ni evento parcial en label; incluir C3 | 3/3 correctas | 3/3 correctas |
| D — Disponibilidad desconocida | No determinable y preguntar; no asumir fin de ventana como disponibilidad | 1/1 correcta | 1/1 correcta |

Ninguna condición aprobó gates. Ambas formularon preguntas sobre disponibilidad en D. Las ocho respuestas contienen JSON dentro de fences pese a pedir solo JSON; el checker lo parseó conservando outputs originales. Esto no es cumplimiento estricto de formato y se reporta para ambas ramas.

## Limitación del protocolo: dos tiempos del estado de label

Los expected fijados antes de ejecutar exigían observed_negative para A2/B2/D1 porque la extracción tiene target=0. La tarea no especificó inequívocamente si label_state debía describir extracción o cutoff. Ambos runners llamaron pending a A2/B2 explicando que al cutoff todavía no estaban disponibles. Baseline llamó unknown a D1 por desconocer su estado al cutoff; treatment llamó observed_negative y aclaró que solo se observaba en extracción posterior.

Los checks literales conservan 3 mismatches de label_state en baseline y 2 en treatment. No se cambian expected después de ver outputs. Estas diferencias no demuestran que el suplemento reduzca errores ni son errores críticos de selección: corresponden a un eje temporal ambiguo en el diseño del autor. El análisis semántico se separa explícitamente del resultado literal.

La próxima prueba debería definir dos campos independientes: estado del outcome en la extracción y disponibilidad para el entrenamiento en T. No se ha ejecutado esa nueva prueba ni corregido retrospectivamente esta.

## Observaciones semánticas

- Las reglas de elegibilidad se aplicaron sin incorporar labels futuras ni convertir pending en negativo.
- Ambos outputs hacen preguntas de confirmación sobre hechos ya declarados. En B, ambos preguntan si cutoff equivale a training_timestamp; conviene declarar esa equivalencia textualmente en el siguiente case.
- En D, baseline propone un intervalo de disponibilidad entre cierre y extracción sin contar con regla de certificación. No inventa una fecha exacta ni toma una decisión de inclusión, pero ese intervalo no está validado por el case; mantenerlo como inferencia no comprobada. Treatment deja la disponibilidad explícitamente desconocida.
- Los outputs citan fechas correctas del calendario de A; algunas frases de baseline como «fin de abril + 7» son menos precisas que inicio del mes siguiente + 7. No hubo fecha de disponibilidad incorrecta en la decisión efectiva de esta ronda.
- Estas observaciones no sustituyen review independiente ni justifican afirmar superioridad general.

## Eficiencia observada

| Condición | Tiempo acumulado, cuatro calls | Coste reportado CLI |
|---|---:|---:|
| Baseline | 47,55 s | USD 0,249146 |
| Treatment | 34,80 s | USD 0,239488 |

Modelo claude-sonnet-5-5, effort medium. Son mediciones de una ejecución por case/condición, con orden alternado; no significancia ni ahorro demostrado. Prompt caching, variación del servicio y distinta longitud de respuestas pueden influir. No se usa score compuesto.

## Integridad e infraestructura

Inputs, expected, pautas y suplemento se congelaron antes de ejecutar; frozen-inputs.json conserva hashes y deterministic-checks.json confirma que no cambiaron. La única diferencia en el payload es el suplemento. Ocho sesiones nuevas sin persistencia, safe-mode, sin herramientas ni MCP; expected nunca se incluyó en el prompt. El mismo autor controla preparación y revisión; el aislamiento de contextos no vuelve independiente la review.

El primer intento baseline A dentro del sandbox falló con ENOTFOUND, coste reportado 0 y sin respuesta evaluable. Se conserva en infrastructure-attempt-01; después la ejecución fuera del sandbox permitió conexión. No se reintentó por mala calidad ni se seleccionaron outputs favorables. El intento de infraestructura no se cuenta como una novena respuesta evaluable.

## Recomendación

Conservar validate-delayed-outcome-targets como conocimiento conforme a su decisión previa. No crear una skill separada ni promover design-validation: las pautas actuales resolvieron la elegibilidad de los cuatro casos. Registrar la ambigüedad del contrato como aprendizaje local; si se repite el problema de representación temporal, revisar una extensión mínima de contrato/template antes de una capacidad nueva.

El error previo del piloto sigue siendo evidencia concreta de outputs, no frecuencia real en clientes. Esta prueba no anula ese fallo ni acredita generalidad. Requiere otros casos más exigentes y review independiente si se busca evidencia de mejora; no modificar Foundry automáticamente.
