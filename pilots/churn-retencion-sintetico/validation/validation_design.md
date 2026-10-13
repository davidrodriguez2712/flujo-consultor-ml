# Diseño de validación corregido — propuesta para revisión

Estado: diseño aprobado por David Rodríguez el 2026-10-07. Este documento corrige los outputs de la comparación exploratoria; no los sobrescribe. No hay modelo entrenado ni gates posteriores aprobados.

## Escenario

Scoring al inicio de cada mes de clientes activos que pueden repetirse. Target: cancelación en el mes que empieza en ese scoring. La label madura al comenzar el mes siguiente + 7 días. Producción real y cadencia de reentrenamiento no han sido evaluadas: el piloto adopta el protocolo siguiente.

## Regla exacta

En una fecha de entrenamiento T, incluir solo labels con `label_available_at <= T`. No usar el flag observed de la extracción como sustituto de esa regla.

Ejemplo: para scoring 2025-07-01, junio madura el 2025-07-08 y no entra al train. Mayo madura el 2025-06-08 y sí puede entrar. Pending nunca se rellena con 0.

## Desarrollo

9 folds mensuales de septiembre de 2024 a mayo de 2025. Cada fold entrena con toda la historia disponible desde febrero de 2024 y evalúa el mes del fold. El primer fold usa febrero–julio: 6 meses. Toda imputación, transformación, selección y fit se aprende solo del train del fold. Parámetros o políticas se seleccionan exclusivamente usando desarrollo.

Los mismos clientes pueden compartirse entre meses: esto reproduce el scoring futuro del mismo universo. customer_id solo es clave/desempate, nunca predictor. No imponer GroupKFold para una pregunta distinta de clientes nuevos. El caso no valida clientes nuevos: no hay nuevas altas después de junio de 2024.

## Evaluación final propuesta

Congelar features, reglas y parámetros después de desarrollo y antes del scoring de julio. Entrenar un modelo fijo el 2025-07-01 con labels ya disponibles (hasta mayo) y puntuar julio–diciembre de 2025 sin reentrenarlo. Esta elección elimina la ambigüedad de usar labels anteriores del test para refits; evalúa extrapolación temporal de un modelo fijo durante seis meses.

No usar labels individuales del test para selección, tuning o ajuste de reglas. No calcular performance de test hasta congelar el protocolo y obtener revisión. Si se quisiera evaluar reentrenamiento mensual, requeriría otro protocolo previamente fijado; no añadirlo después de observar el test.

## Scoring sin label

Enero de 2026 puede puntuarse como simulación prospectiva, pero no se evalúa con la extracción del 2026-01-15: su label madura el 2026-02-08.

## Features y joins

Excluir outcomes, cancellation_at, label_status y metadata de labels como predictors; no utilizar IDs ni constantes como señal. Agregar tickets por cliente/scoring antes de unir, o usar el conteo existente sin doble suma. Missing de actividad no equivale a cero: la regla de imputación se fija en train. Las fechas de disponibilidad gobernarán las uniones.

## Métricas y evidencia

Precision@50 y Recall@50 mensuales; Lift@50 como complementaria propuesta. Comparar con azar por mes y con un baseline analítico simple. MRR en riesgo no demuestra efecto causal ni ROI. Los datos son sintéticos.

Checks de filas, positivos y ventanas en `analysis/outputs/proposed-split-checks.json`. Se comprobaron las fechas a partir de las labels del fixture; no se computaron métricas predictivas de test. No estimar positivos por mes a partir de una media global.

## Límites

La comparación inicial de design-validation no demostró mejora consistente, tuvo errores temporales y no recibió review independiente. La versión experimental se conserva. Este diseño corregido fue aceptado por el reviewer. Los outputs y gates posteriores requieren su propia revisión.
