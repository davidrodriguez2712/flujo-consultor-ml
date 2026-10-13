---
skill: understand-dataset
version: 0.1.0
fecha: 2026-10-09
proyecto: retail-valor-90d-publico
inputs:
  - path: data/raw/online_retail_II.xlsx
    sha256: bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980
estado: Auditoría completa; contratos y calidad pendientes de revisión humana
---

# Comprensión de Online Retail II

## Resumen

Dos hojas del mismo libro, 1,067,371 filas y ocho columnas de negocio por hoja. Se normalizan nombres y tipos en una copia con source_sheet/source_row; el original permanece intacto. Unidad probable: línea de factura/producto, no cliente. Target propuesto: ventas positivas por cliente durante los 90 días posteriores a un cutoff. No es una columna existente, ni fue calculado. Su horizonte debe estar completo; la disponibilidad operacional de transacciones es desconocida.

La historia parece permitir formular una evaluación temporal, pero aún faltan aprobar población, reglas de compra, solapamiento, cutoffs y disponibilidad. No se declara listo para Modeling.

## Hallazgos

### Crítico

- [Hecho] Las hojas comparten ocho días y 1,088 facturas. Hay 22,202 patrones idénticos y 22,523 filas coincidentes al conservar multiplicidad por hoja. Evidencia: `reports/discovery/sheet_overlap.json`.
- [Hipótesis] Tratar ambas hojas como particiones independientes y sumar sin reconciliar podría duplicar ventas, features y labels. Se propone reconciliación entre hojas antes de generar snapshots, manteniendo trazabilidad; aún no se aplica.

### Alto

- [Hecho] 243,007 filas (22.77%) carecen de ID. La cobertura de clientes individuales no representa todo el archivo. Evidencia: `source_audit.json`, global.missing.customer_id.
- [Hecho] 19,494 filas tienen factura c/C; 22,950 tienen cantidad negativa. Hay una factura c/C con cantidad positiva: ninguna regla debe depender solo del signo. Evidencia: global.cancellation_rows y cancellation_positive_quantity_rows.
- [Hecho] Hay 5 precios negativos y 6,202 precios cero. Sus significados requieren tratamiento explícito; no se corrigen por valor absoluto ni se imputan como compras.
- [Hecho] La documentación no proporciona timestamps de ingestión ni historial de revisiones. [Hipótesis] La fecha de factura podría no coincidir con disponibilidad efectiva. No certificar leakage ausente sin reconocer ese supuesto.

### Medio

- [Hecho] 34,335 filas extra son idénticas en las ocho columnas normalizadas, sin provenance. El conteo incluye repeticiones dentro de hojas y solapamiento entre ellas; no significa que todas puedan eliminarse. Dentro de cada hoja hay 6.865 y 5.268 filas extra idénticas.
- [Hecho] invoice_id + stock_code tiene 45,947 filas extra; no es una clave única de línea. Repetir un producto puede ser legítimo. No hacer join de líneas solo por esas claves.
- [Hecho] Códigos POST/DOT tienen descripciones de postage, C2 carriage, D discount, M manual; BANK CHARGES y ADJUST son ejemplos que requieren clasificación. El patrón de código inusual es una heurística, no prueba de que el producto sea inválido. Evidencia: `code_descriptions.json`.
- [Hecho] El rango global no es monótono en orden de archivo por el solapamiento; cada hoja sí es monótona. Los días sin registros no prueban fallo de cobertura.

### Informativo

- [Hecho] Se observan 5,942 IDs, 53,628 facturas y 43 países, antes de exclusiones. Cantidad, precio y fecha se parsean sin errores detectados. La población combina países y clientes mayoristas según la ficha: no asumir consumidores finales de Reino Unido únicamente.

## Evidencia

| Hoja | Filas | Fecha inicial | Fecha final | IDs ausentes | Duplicados exactos extra |
|---|---:|---|---|---:|---:|
| Year 2009-2010 | 525.461 | 2009-12-01 | 2010-12-09 | 107.927 | 6.865 |
| Year 2010-2011 | 541.910 | 2010-12-01 | 2011-12-09 | 135.080 | 5.268 |

- `load_metadata.json`: schema, mapping, tipos y parse_errors por hoja.
- `source_audit.json`: missing, cardinalidades, claves, días, cantidades/precios y duplicados.
- `sheet_overlap.json`: intersecciones y multiplicidad, sin join cartesiano.
- `data/interim/manifest.json`: copia normalizada sin filtros; misma cantidad de filas.
- `tests-overlap-green.log`: nueve tests pasan; RED inicial y RED del solapamiento conservados.

El screening positivo (cantidad/precio > 0, factura no c/C) identifica 1,041,670 líneas y 805,549 con ID. El importe preliminar sin ID representa 15.40% del importe positivo bruto de ese screening. Estas cifras aún incluyen duplicación y códigos no resueltos: no son ventas finales ni KPI aprobado.

## Preguntas abiertas

1. ¿Reconciliar entre hojas por patrón completo conservando la mayor multiplicidad observada, o usar particiones temporales con una hoja por tramo?
2. ¿Qué regla mínima defendible separa mercancía, cargos y ajustes, sin inferir solo por el nombre?
3. ¿Cómo tratar repeticiones dentro de la misma factura cuando falta un identificador de línea?
4. ¿Qué población comercial debe representar el ranking y qué cobertura sin ID queda excluida?
5. ¿Cómo fijar el supuesto de disponibilidad y medir su efecto en labels/fit?
6. ¿Qué cutoffs completos permiten comparar períodos independientes suficientes?

## Recomendaciones

Revisar Discovery y aprobar Framing antes de limpieza orientada al target. Mantener fuente y auditoría congeladas. Resolver solapamiento con un contrato trazable y no borrar todos los duplicados. Separar hechos de supuestos; evaluar explícitamente el efecto de cualquier exclusión. No entrenar, generar labels ni elegir modelos en esta etapa.
