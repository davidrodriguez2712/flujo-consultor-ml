# Mejora del flujo: correspondencia entre cifras, etiquetas y períodos

Fecha: 2026-10-09. Alcance aprobado: checklist, workflow, manual generado y ejemplo local.

## Cambios

- Findings y QA identifican métrica, población, unidad, método y período con keys explícitas; incluyen un registro de contraste entre afirmación y artifact fuente.
- El workflow define cómo interpretar “último” según método/población, elegibilidad y períodos completos. Distingue extracción, scoring, observación y outcome; pide revisar ventanas, límites y madurez cuando importen.
- El manual generado referencia el procedimiento y declara el límite de automatización.
- El compiler incluye el template `templates/findings-and-qa.md` en proyectos nuevos. Los recursos empaquetados de workflow y template coinciden con las fuentes del OS.
- Las correcciones conservan el original y registran fuente, motivo e impacto sobre la aceptación afectada.

No se modificaron los pilotos cerrados ni el Foundry. No se añadieron gates o cambios al esquema de estado.

## Verificación

Test nuevo del compiler: falló por ausencia del template antes del cambio y pasó tras incluirlo. Verifica que el archivo existe y figura en el manifest inicial.

Suite completa: `.venv/bin/python -m pytest` — **146 passed**, 4.34 s. Los tests del proxy se ejecutaron con permiso para localhost y proveedores simulados. Costo API **US$0**.

Ejemplo repetible desde el checkout:

```sh
PYTHONPATH=src .venv/bin/python docs/acos/validation/label-period-example.py
```

El ejemplo genera un proyecto con el compiler real. Una fuente hipotética desordenada contiene:

| Método | Cutoff | Outcome completo | Valor |
|---|---|---|---|
| baseline | 2026-06-01 | Sí | 0.25 |
| baseline | 2026-12-01 | No | 0.8 |
| challenger | 2026-09-01 | Sí | 0.9 |
| baseline | 2026-09-01 | Sí | 0.6 |

Seleccionar la primera fila produciría una cifra válida (0.25) atribuida incorrectamente al “último período completo del baseline”. La selección por keys, elegibilidad y fecha obtiene septiembre (0.6); diciembre es el último observado, pero está incompleto.

Resultado: PASS en las 24 permutaciones de filas. El ejemplo también rechazó keys duplicadas y ausencia de períodos completos. Conservó un registro original y una corrección separados. [Resultado JSON](2026-10-09-label-period-example.json).

## Revisión y límites

Revisión nativa del alcance y consistencia documental; no constituye revisión independiente ni evaluación comparativa de skills. El ejemplo usa una regla explícita de elegibilidad y comprueba identidad por keys; no interpreta automáticamente texto libre ni valida entregables completos.

`acos validate` mantiene sus checks y no interpreta títulos, leyendas o períodos de los artifacts. La mejora se distribuye en proyectos nuevos compilados desde este checkout, sin actualizar snapshots existentes ni publicar una release.

## Estado de las tres mejoras priorizadas

1. Evidencia congelada frente a documentos vivos: implementada y verificada.
2. Recorrido de reproducción y serialización: implementado y verificado.
3. Correspondencia entre cifras, etiquetas y períodos: implementada y verificada.

La adopción conjunta en un engagement nuevo y la eficacia de las capacidades requieren evidencia posterior; estas verificaciones no promueven madurez del Foundry.
