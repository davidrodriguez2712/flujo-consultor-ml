---
case_id: N03
skill: detect-leakage
---

# Comportamiento esperado

Fit_transform se ajusta sobre todo data antes de particionar; evaluación futura influye en parámetros del scaler. Preprocessing/train-test contamination confirmado por código, aunque amount disponibleal scoring no sea intrínsecamente futura. Remedio fit solo train y transformevaluation; Si posteriormente se usa CV, el fit debe estar dentrofold; en este caso sin CV es recomendación condicional/opcional, no requisito de PASS. No afirmar métricas del modelo ni que basta eliminar outliers o cambiar scaler. Labels futuros de evaluación legítimos.

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
