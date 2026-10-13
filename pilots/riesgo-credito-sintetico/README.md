# Piloto sintético de riesgo de crédito

Estado: COMPLETED. Las siete etapas y los doce gates fueron aprobados por David.

## Empezar

```sh
cd pilots/riesgo-credito-sintetico
acos status
acos next
acos validate
```

Leer [MANUAL](MANUAL.md), [paquete de Handoff](handoff/review.md) y [diccionario](data/dictionaries/README.md). Consultar [cierre](handoff/closure.md). `acos validate` devuelve PASS; status/next no muestran gates pendientes.

## Reproducir datos

Desde esta carpeta, con Python 3.11 o superior:

```sh
python analysis/generate_synthetic_data.py --output /tmp/acos-credit-replay
```

Usar una ruta nueva. El generator rechaza sobrescribir las fuentes. La seed predeterminada es 20261008; comparar los hashes CSV con `data/raw/manifest.json`. El generator requiere solo stdlib. Las pruebas necesitan pytest.

## Límites

Datos ficticios. Sin clientes, políticas crediticias, moneda ni mercado reales. Sin acceso a APIs. Las decisiones históricas pertenecen a la simulación; no son recomendaciones. El piloto completó development y evaluación final sintética; Handoff y cierre están aprobados. Los outcomes de rechazadas no están disponibles.
