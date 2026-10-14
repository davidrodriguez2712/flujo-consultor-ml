# detect-leakage 0.2.3 — dos corridas nativas L03

Fecha: 2026-10-13. David adjudicó el L03 nativo 0.2.2 como **aceptable con reservas** y autorizó US$0.03 adicionales (techo US$0.18). Canonical, case, expected, workflow y transporte congelados intactos. Madurez: experimental, sin promoción.

## Cambio evaluado
0.2.3 añade a la receta de salida: un dato por sección (sin hechos legítimos como el target en Hallazgos, Preguntas solo con lo no pedido, sin repetir la skill del frontmatter). Formato raíz para compatibilidad con el transporte congelado, que lee `version` en la raíz; el borrador `metadata:` está en `draft-023/`.

## Resultados (L03 nativo, treatment, una corrida cada una, sin reparar ni reintentar)
| Corrida | Cap | Runtime | Contrato | Palabras reporte/final | Coste US$ |
|---|---:|---|---|---:|---:|
| 0.2.2 (referencia, CLI 2.1.296) | 4096 | PASS | FAIL | 515 / 60 | 0.004567 |
| 0.2.3 `native-results-023` (CLI 2.1.299) | 4096 | **FAIL: `max_tokens`** (4096 salida, 2709 thinking), sin reporte | no evaluable | — | 0.004386 |
| 0.2.3 `native-results-023b` (CLI 2.1.299) | 8192 | PASS | **FAIL: 532 > 500** | 532 / 40 | 0.003878 |

El segundo intento no fue un reintento idéntico: cambió el cap tras diagnosticar la truncación. No hubo más reintentos.

## Lectura
- **La hipótesis de redundancia no se confirma:** 0.2.3 produjo 532 palabras, más que 0.2.2 (515). Con una sola corrida por versión no se puede atribuir la diferencia a la skill (varianza, cap y CLI distintos).
- Contenido de 023b (lectura del autor, no revisión independiente): No determinable, sin invalidez ni disponibilidad presumida, ambas condiciones explícitas. Persisten Preguntas que reformulan el hallazgo y un hallazgo único extenso.
- Hipótesis nueva, **sin probar**: el límite de 500 palabras incluye frontmatter con 4 hashes y cinco títulos (~100 palabras de estructura fija), así que pedir brevedad a la skill no basta. Opciones: subir el límite del contrato (cambia el criterio; requiere decisión humana y no aplicarlo retroactivamente) o reducir el esquema obligatorio.
- Desviaciones: el CLI cambió de 2.1.296 a 2.1.299 (guard de versión detuvo el primer lanzamiento sin gasto; se refirmó solo `cli_version`); la compatibilidad del transporte con 2.1.299 no estaba verificada, aunque ambas corridas completaron el runtime. No comparables estrictamente con 0.2.2.

## Coste
Acumulado US$0.14846196 de US$0.18; saldo US$0.03153804 (estimado por ledger, solo Anthropic). Pago detenido. El micro textual y la comparación baseline vs. treatment no se ejecutaron: ninguno resuelve el fallo nativo de extensión.

## Evidencia
`native-package-023/`, `native-package-023b/` (manifests `c6852a55…`, `61286f80…`), `native-approval-023*.json`, `native-results-023/`, `native-results-023b/`, `HUMAN_ADJUDICATION_L03.md`.
