---
skill: design-validation
version: 0.1.0
fecha: 2026-10-09
proyecto: retail-valor-90d-publico
inputs:
  - "framing/retail_contract.yaml sha256:0e537ce003ac0c125d89f5a0aa301f3c29a09316f3e90d985a4b82cc642c6ab4"
  - "data/interim/manifest.json sha256:7210b8d55b9d173cec140dd31c97e3600c8a841aa9fd593fd9b053ba04a2a83a"
  - "reports/diagnosis/cutoff-proposal.json sha256:edcc0052974dd23a464bb0a9a828679732b36a8d483d9318f9352a0d0895e0bb"
estado: Diseño propuesto; pendiente revisión humana.
---
# Diseño de validación

## Resumen

Walk-forward para volver a priorizar clientes conocidos cada mes. Cuatro evaluaciones development y una evaluación final out-of-time. Es viable para un benchmark histórico bajo disponibilidad inmediata supuesta; no acredita viabilidad operacional con retrasos desconocidos.

## Objetivo de validación

Estimar la capacidad de priorizar 100 clientes por sus ventas válidas observadas durante los siguientes 90 días, usando solo su historial anterior al cutoff. No estimar efecto de contactarlos.

## Estructura de datos relevante

Transacciones repetidas por cliente y fecha; unidad futura cliente × cutoff. Ventana histórica 180 días, outcome 90 días, regresión positiva con posibilidad de cero. 5.852 clientes observados en compras válidas; elegibilidad por período entre 2.658 y 3.465. No se calculó distribución de targets ni balance por partición: corresponde a ejecución posterior, sin inspección anticipada del holdout.

## Estrategia recomendada y definición de splits

- Model development: 2010-09-01, 2010-12-01, 2011-03-01 y 2011-06-01. Entrenar en snapshots mensuales maduros al fit; evaluar el horizonte siguiente completo.
- Final evaluation: 2011-09-01, hasta 2011-11-30 exclusivo. Elegir método previamente con development; abrir resultados una sola vez.
- Out-of-time: el mismo holdout final cumple este propósito; no se inventa otro conjunto independiente.
- Operational evaluation: mismo ranking Top-K y población por método; resultados por período y suma development. Capacidad 100 simulada.

El último cutoff mensual con horizonte completo se eligió por cobertura, no desempeño. Las métricas y labels del holdout quedan reservados. El diagnóstico descriptivo global sí vio distribución de toda la fuente; explicitar esta limitación de ceguera.

## Diseño de cross-validation

Expanding window de snapshots maduros, sin tuning ni nested CV. Development separado >=90 días para evitar solapamiento de sus outcomes. Los snapshots mensuales train pueden solapar outcomes: dependencia declarada, sin intervalos estadísticos IID. Primer fit solo tiene snapshot 2010-06-01. Al menos dos períodos requeridos; hay cuatro.

## Manejo de entidades

Compartir clientes entre train y evaluación corresponde a puntuar clientes conocidos en fechas posteriores. ID solo identifica/desempata, nunca feature. No se está evaluando generalización a entidades nuevas. No se afirma ausencia de overlap de clientes: es intencional.

## Salvaguardas de leakage

Historia en [cutoff-180d,cutoff), target en [cutoff,cutoff+90d); train exige label_end <= fit_at. Transformaciones/modelo se ajustan dentro de cada fit, nunca globalmente. No target encoding, resampling ni búsqueda de hiperparámetros. La fecha de ingestión no existe: label delay real es No determinable; base retrospectiva 0d es un supuesto aprobado. Sensibilidad hipotética +7d deja el primer fit sin snapshot maduro y resta uno en los demás. No confundir este check con disponibilidad real acreditada. Auditoría posterior del pipeline: detect-leakage.

## Métricas

Selección: suma de ventas válidas futuras en Top-K por development. MAE, fracción de ventas elegibles capturada, cobertura, estabilidad y concentración son complementarias. ROC-AUC y Precision@K de clasificación no aplican a este target monetario continuo. No optimizar MAE cuando la decisión primaria es ranking. Reglas exactas en validation/evaluation_contract.yaml.

## Riesgos, alternativas descartadas y preguntas abiertas

Random holdout: mezcla futuro y pasado en una decisión mensual. GroupKFold: estima clientes nuevos, distinto escenario. TimeSeriesSplit por fila: unidad transacción y ventanas de target no representan cliente × cutoff. Nested CV/tuning: innecesario con dos modelos de configuración fija y escasez temporal. No añadir embargo arbitrario: madurez completa del target ya se exige; latencia operacional requiere datos adicionales.

Hay pocas estaciones/períodos y concentración de ventas; no extrapolar a otro retailer o campaña. Confirmar latencia, identidad estable y naturaleza de repeticiones si fuera despliegue real. La deduplicación interna alternativa reduce ventas 0,329% sin cambiar cobertura global de clientes; no demuestra ausencia de impacto local.

Implementación posterior: congelar contrato tras aprobación, construir snapshots con provenance, comprobar límites/labels maduras y luego entrenar. Esta skill diseñó el esquema; no ejecutó splits ni entrenó. Uso experimental aplicado al caso, sin demostrar eficacia ni promover madurez Foundry.
