# Runner de selección operacional

Versión `0.1.0`; utilidad local del checkout, sin cambios en los comandos instalados de ACOS. Usa [schema común 0.1.0](../../../schemas/selection-audit-0.1.0.schema.json). Su transporte se deriva del runner temporal 0.2.0, conservando esa utilidad y sus snapshots anteriores intactos.

```sh
.venv/bin/python scripts/evaluations/selection_runner.py \
  --payload-file ruta/payload.txt \
  --output-dir ruta/intento-nuevo
```

Modelo por defecto solicitado: `claude-sonnet-5-5`; effort solicitado medium. La configuración efectiva solo se acredita cuando el envelope la expone. Cada llamada utiliza un cwd temporal vacío, sin herramientas/MCP/persistencia según flags solicitados. La carpeta destino debe ser nueva.

## Separación de resultados

1. `runtime_success`: CLI completó exitosamente.
2. `schema_conformant`: Pydantic estricto y guards locales de texto no blanco, Unicode válido y unicidad de IDs. El JSON Schema enviado no expresa todos esos guards; no equivale a conformidad nativa únicamente.
3. Contenido: checker externo contra expected, más revisión semántica de razones, estimand, supuestos y preguntas. El runner conserva `content_validation=NOT_RUN` y nunca lee expected.

Archiva payload, schema, argv/cwd, stdout/stderr, raw, structured_output y metadata. No extrae JSON del texto result, no repara ni reintenta. Un objeto inválido se conserva y se reporta. El runtime nativo puede realizar pasos internos para obtener su respuesta estructurada.

## Semántica del output

- `selected_ids`: selección final en el orden pedido.
- `risk_ranking_ids`: ranking descriptivo completo, separado de una política por valor.
- `selection_status`: decisión determinada o información insuficiente. `effective_k=null` con selected_ids vacío significa decisión pendiente; con selección vacía determinada, effective_k=0.
- `output_type`, `feasibility`, `optimality` y `causal_identification.status` describen dimensiones distintas. Ninguno aprueba una acción.
- `total_cost` y `expected_net_value`: valores del conjunto según unidades y objetivo provistos; no restar de nuevo un coste ya incluido en valor neto.
- Métricas con población, valor nullable y estado por métrica; null no se convierte en cero.
- Gate humano se comprueba externamente. El schema admite otros valores de gate y decisiones erróneas para que pueda medirse el fallo.

## Checker y oracle

[selection_checker.py](../../../scripts/evaluations/selection_checker.py) compara miembros, orden, ranking, capacidad, costes/valor, factibilidad, optimalidad, métricas/población, estado causal y gate por separado; conserva mismatches, sin score compuesto. Los números usan tolerancia absoluta 1e-8 y rechazan booleans. Texto de estimand y razones se revisan semánticamente.

Su enumerador solo cubre selección aditiva indivisible de hasta 20 registros, con capacidad y presupuesto. No representa routing, interacciones, decisiones reales bajo incertidumbre ni optimización general. En una evaluación, derivar expected también por un cálculo independiente: comparar un oracle consigo mismo no valida el criterio.

El checker no determina verdad de negocio ni prueba que los supuestos del input se cumplan fuera del caso ficticio. Un exit code 0 significa que el checker se ejecutó; hay que inspeccionar los resultados. El runner tampoco identifica mejora respecto de baseline por completar una llamada.
