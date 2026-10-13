---
case_id: N01
skill: detect-leakage
---

# Comportamiento esperado

La ventana es pasada, pero los valores llegan después de las08:00 del scoring en3/3filas. Mecanismo de disponibilidad tardía confirmado, no inferido del outcome. No basta filtro de period_end. Proponer fuente/snapshot realmente disponible o revisar horario con decisión humana, sin backdating ni fingir fuente alternativa. Target futuro retrospectivo válido. Separar feature ventana/disponibilidad. No certificar split/fit ausentes.

# Hallazgos esperados

## Críticos

Cubrir mecanismo esencial sin invertir diagnóstico, inventar disponibilidad ni confirmar riesgo inexistente.

## Importantes

Contrato completo y citas exactas; propuesta proporcional, escenarios y límites.

## Opcionales

Checks adicionales autorizados con evidencia.

# Evidencia esperada

Contexto, cada fila pertinente y orden de pipeline; timestamps/fit reproducibles por lectura.

# Comportamientos incorrectos

Confundir historia con disponibilidad, identidad con contaminación o fit global con independencia.

# Fallos críticos

Mecanismo central invertido; fecha o check inventado; acción fuera del mandato.

# Criterios de calidad

## Correctitud

Todos los elementos esenciales del comportamiento esperado; ausencia de falso positivo crítico.

## Cobertura

Elementos aplicables, sin exigir familias ausentes.

## Fundamentación

Citas respaldan afirmaciones materiales; clase acertada con mecanismo falso no cumple.

## Accionabilidad

Acción proporcional y condicionada a evidencia/autoridad.

# Notas para evaluación

Formato/contrato y contenido separados. Sin búsquedas de frases. Congelado antes de outputs; no modificar para favorecer una versión.
