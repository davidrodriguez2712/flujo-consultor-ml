# Contrato temporal de labels

Versión documental: `0.1.0`. Estado: propuesto, local, no ejecutado. [Alcance compartido](README.md).

## Propósito

Separar lo observado en una extracción posterior de lo disponible al entrenar. Resuelve la ambigüedad de `label_state` y evita inventar fechas o intervalos de disponibilidad.

## Inputs mínimos

| Campo | Significado |
|---|---|
| `extraction_timestamp` | Instante del snapshot que se está leyendo |
| `training_timestamp` | Instante en que se habría construido el conjunto de entrenamiento |
| `prediction_timestamp` | Instante al que deben corresponder las features de una fila |
| `feature_available_at` | Disponibilidad de cada feature usada, o máximo comprobado sobre ellas |
| `outcome_window_start`, `outcome_window_end` | Ventana del target, con límites inclusivos/exclusivos declarados |
| `target` | Valor observado o `null`; su significado no implica certificación |
| `label_available_at` | Disponibilidad certificada del target para entrenamiento, o `null` |
| `certification_rule` | Cuándo un outcome es definitivo; si admite positivos tempranos y cómo trata negativos |
| `availability_rule` | Comparador de disponibilidad; por ejemplo `<=` |

Usar timestamps con zona horaria y precisión declarada. `cutoff` no sustituye silenciosamente a `training_timestamp`: si existe, declarar qué limita y su relación con los demás instantes. Un delay derivado requiere regla y origen explícitos; no confundir fin de ventana, extracción y disponibilidad certificada.

## Output por fila

| Campo | Valores |
|---|---|
| `outcome_state_at_extraction` | `observed_positive`, `observed_negative`, `pending`, `unknown` |
| `label_availability_at_training` | `available`, `unavailable`, `indeterminate` |
| `train_eligibility` | `eligible`, `exclude`, `indeterminate` |
| `reason` | Reglas, timestamps y evidencia usados; sin completar información ausente |

`observed_positive/negative` requiere certificación al instante de extracción. `pending` significa que la regla conocida aún no permite certificar; `unknown`, que falta información para establecer el estado. Un cero provisional no es `observed_negative`. Un evento temprano solo es positivo definitivo si lo autoriza la regla del target.

Disponibilidad al entrenar: `available` si la fecha certificada cumple el comparador y existe el valor requerido; `unavailable` si una regla conocida prueba que todavía no estaba disponible; `indeterminate` si faltan fechas o certificación. Observar el valor después no demuestra disponibilidad antes.

Para la elegibilidad deben cumplirse todas las reglas del case: features disponibles al predecir, label disponible al entrenar y condiciones de población/ventana. Una exclusión comprobada produce `exclude`; si no hay exclusión comprobada y falta una condición, `indeterminate`. Solo todas las condiciones comprobadas permiten `eligible`. Una fila excluida conserva el estado del outcome en extracción; no se cambia a `pending` por estar excluida.

Inputs contradictorios, como certificación posterior a extracción pero estado declarado definitivo sin otra regla, requieren reportar el conflicto; no resolverlo inventando una fecha.

## Ejemplo ilustrativo

Regla: negativo certificado al inicio del mes siguiente más siete días; igualdad `<=` admitida. Ventana `[2025-06-01, 2025-07-01)`, todas las features disponibles antes del scoring. `training_timestamp=2025-07-01T00:00:00Z`, `extraction_timestamp=2025-08-15T00:00:00Z`, target negativo certificado disponible el 8 de julio.

```yaml
id: customer-02
outcome_state_at_extraction: observed_negative
label_availability_at_training: unavailable
train_eligibility: exclude
reason: La etiqueta está certificada en extracción, pero disponible después del entrenamiento.
```

## Criterios de aceptación para otra ronda

- Fijar expected separado para cada eje; no un único estado ambiguo.
- Comprobar casos de igualdad y un instante posterior con la precisión declarada.
- Una fecha desconocida no produce un intervalo estimado sin fuente.
- Un outcome pendiente o desconocido no se convierte en negativo.
- Una feature futura excluye la fila aunque el label esté disponible.
- Incluir un ejemplo realmente elegible, un positivo temprano permitido y otro no certificado.
- Las razones deben citar la misma regla que produce la decisión; acertar la clase no compensa una justificación inventada.

Estos criterios aún no son checks implementados ni evidencia de mejora. [Contrato de ejecución](execution-provenance.md).
