# Plantillas de findings y QA

Aplicar al nivel de riesgo y tipo de entrega. No llenar cada campo si no aplica; la ausencia de una comprobación debe quedar clara cuando importe.

## Finding trazable

Usar para hallazgos que sostienen recomendación, priorización o decisión.

```markdown
### [F-##] [afirmación concisa]

- Tipo: [hecho descriptivo / diagnóstico / predicción / estimación causal / hipótesis]
- Relevancia para la decisión:
- Métrica y definición / población / unidad:
- Período y cutoff (inicio/fin, inclusión de límites, timezone si aplica):
- Keys que identifican el resultado en la fuente:
- Evidencia: [tabla/figura/query/fuente + versión/ruta]
- Método/denominador/comparador:
- Incertidumbre o limitación:
- Alternativas/explicaciones pendientes:
- Confianza: [nivel y razón, no solo etiqueta]
- Próximo paso o decisión que informa:
```

## Checklist de revisión de entrega

Usar antes de compartir una recomendación, análisis o artifact con el cliente. Ajustar el rigor al riesgo; un reporte ejecutivo y un modelo operativo requieren evidencias distintas.

```markdown
# QA — [entregable/version]

- Reviewer / fecha:
- Audiencia y decisión:
- Nivel de riesgo:

## Contenido y evidencia
- [ ] Respuesta y recomendación coinciden con el encargo aprobado.
- [ ] Las afirmaciones materiales apuntan a evidencia reproducible o fuente verificable.
- [ ] Totales, denominadores, períodos, moneda/unidades y redondeos reconciliados.
- [ ] Cada cifra material corresponde a su métrica, población, unidad, método y período mediante keys explícitas de la fuente.
- [ ] Títulos, leyendas, tablas, texto y logs usan las mismas definiciones y fechas que el artifact fuente.
- [ ] “Último” se deriva de fechas/cutoffs entre períodos elegibles y completos, no de la posición de una fila; se declara la fecha concreta.
- [ ] Ventanas, límites incluidos/excluidos, timezone y madurez del outcome se comprobaron cuando afectan la interpretación.
- [ ] Ordenar o filtrar filas no cambia la identidad del resultado citado; duplicados o keys ambiguas se resolvieron o declararon como bloqueo.
- [ ] Asociación, predicción y causalidad se nombran correctamente.
- [ ] Limitaciones, supuestos y resultados negativos pertinentes están visibles.
- [ ] No se extrapola a población o período sin sustento.

## Uso y presentación
- [ ] Próxima acción, responsable, costo/riesgo y dependencias son claros cuando aplican.
- [ ] Lenguaje/gráficos adecuados a la audiencia; definiciones necesarias incluidas.
- [ ] Privacidad, anonimización y permiso de distribución verificados.
- [ ] Links/archivos abren desde el entorno esperado.

## Resultado
- Estado: [PASS / PASS con límites / REVISE / BLOCKED]
- Hallazgos y severidad:
- Correcciones/re-chequeos:
- Pendientes y owner:
- Aprobación humana requerida por:
```

## Registro de contraste entre cifra y etiqueta

Usar para las afirmaciones materiales; no exige transcribir todas las celdas. Resolver la identidad del resultado antes de comparar su valor.

| Afirmación / ubicación | Artifact fuente y versión | Keys: métrica, método, población y período/cutoff | Unidad / denominador | Valor esperado y redondeo | Etiqueta/valor publicados | Resultado y corrección |
|---|---|---|---|---|---|---|
| | | | | | | |

Si no se puede identificar una fila única con las keys acordadas, registrar la ambigüedad antes de aceptar la cifra. Un valor que existe en la fuente puede estar atribuido a otro período o método. Ante una corrección, conservar el original y registrar ubicación, etiqueta anterior, valor/período correctos, fuente, motivo, impacto y revisión del alcance afectado. Aplicar el procedimiento de evidencia en [`../workflow/execution-and-qa.md`](../workflow/execution-and-qa.md).
