# Contrato de evidencia y claims

Versión documental: `0.1.0`. Estado: propuesto, local, no ejecutado. [Alcance compartido](README.md).

## Propósito

Comprobar la proposición exacta y todas sus premisas. Separar hechos, cálculos, efectos, grado de certeza, supuestos y recomendaciones; un ID válido no demuestra soporte completo.

## Inputs mínimos

- Decisión, audiencia, owner y límites de autoridad.
- Fuentes con ID, contenido, población, período, unidad y límites conocidos.
- Contratos con IDs propios: definiciones, denominadores, guardrails y umbrales.
- Claims del borrador con IDs y texto exacto. Separar proposiciones compuestas antes de fijar expected.
- Regla para interpretar el grado de certeza: diseño, intervalo/nivel reportado y supuestos. No inventar umbrales estadísticos.
- Entregable requerido y evidencia que podría cambiar la decisión.

El contexto también puede contener premisas materiales. Si proporciona un umbral, registrarlo como fuente/contrato referenciable; no obligar al agente a citar una fuente que no lo contiene.

## Clasificación de claims

| Estado | Regla |
|---|---|
| `supported` | La evidencia sustenta la proposición con su alcance y grado de certeza |
| `contradicted` | La evidencia refuta esa proposición aritmética o lógicamente |
| `unsupported` | No hay soporte suficiente ni refutación suficiente |

Evaluar primero qué se afirma. «El efecto real es positivo» no es lo mismo que «está demostrado que el efecto es positivo». Un intervalo que incluye cero no demuestra un efecto negativo. Si la fuente indica que no hay evidencia concluyente al nivel definido, puede contradecir la afirmación de certeza sin refutar el signo real del efecto. El expected debe evaluar la misma proposición que el borrador.

Exposición económica no identifica beneficio incremental. Datos de una muestra de riesgo no identifican automáticamente tasas poblacionales ni la dirección del sesgo. Una asociación, diferencia temporal o baseline previo aislado no identifica causalidad. Para claims causales exigir diseño, estimand y supuestos explícitos.

## Output propuesto por claim

- `claim_id`, `statement` y `claim_kind`: por ejemplo `observation`, `calculation`, `causal_effect` o `evidence_certainty`.
- `status`, `reason`, alcance y `evidence_ids`.
- `premises`: proposiciones necesarias con las referencias que sustentan cada una.
- `derivation`: cálculo/regla y unidades cuando corresponda.
- `unsupported_premises`: premisas faltantes; no reemplazarlas por otras fuentes próximas.

Registrar supuestos separadamente con motivo y owner pendiente cuando no esté confirmado. Una recomendación debe identificar qué claims la justifican, qué no se sabe y qué evidencia concreta permitiría reconsiderarla.

## Ejemplo ilustrativo: guardrail

Inputs: E2 registra quejas treatment 8% y control 2%, mismo período/definición; G1 fija incremento máximo de 2 pp, igualdad permitida. No hay permiso para modificar G1.

```yaml
claim_id: CLM-guardrail
statement: El incremento observado de quejas supera el máximo autorizado.
claim_kind: calculation
status: supported
evidence_ids: [E2, G1]
premises:
  - statement: Las tasas comparables son 8% y 2%.
    evidence_ids: [E2]
  - statement: El incremento máximo autorizado es 2 pp.
    evidence_ids: [G1]
derivation: 8% - 2% = 6 pp; 6 pp > 2 pp.
unsupported_premises: []
```

La superación descriptiva del umbral no afirma por sí misma significancia estadística ni un efecto poblacional confirmado. Si el contrato exige otro estimand o incertidumbre, no sustituirlo por esta diferencia puntual.

## Criterios de aceptación para otra ronda

1. Verificar existencia de cada ID y soporte semántico de cada premisa; reportar ambos checks por separado.
2. Recalcular totales, ratios y unidades con denominadores pertinentes. Fracción 0–1, porcentaje y puntos porcentuales son magnitudes diferentes.
3. Separar evaluación del efecto y evaluación de la certeza. Un expected ambiguo se registra como problema del criterio, sin recalificación silenciosa.
4. Conservar `null` y su motivo cuando un impacto/ROI no esté identificado. No convertir exposición o asociación en retorno.
5. Evaluar condiciones futuras de la recomendación: una medición previa por sí sola no basta para autorizar una conclusión causal.
6. Incluir claims realmente sustentados y una recomendación positiva justificada, además de errores y falta de información. No resolver los casos particulares dentro de sus inputs.
7. No inventar owner, presupuesto, fecha o permiso. Distinguir propuesta de decisión aprobada.

Estos criterios precisan la tarea; no prueban eficacia del template ni autorizan delivery externo. [Contrato de ejecución](execution-provenance.md).
