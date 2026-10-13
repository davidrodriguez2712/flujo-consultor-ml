# Mejora del flujo: reproducción y fronteras de serialización

Fecha: 2026-10-09. Alcance aprobado: pautas, templates, manual generado y ejemplo local.

## Cambio y motivo

El incidente del piloto retail mostró que omitir escrituras y lecturas CSV podía cambiar los scores, aunque los inputs parecieran equivalentes dentro de tolerancia. El procedimiento ahora registra el recorrido completo, entorno, comandos, formatos, parsing y criterios de comparación anteriores al run.

- `workflow/execution-and-qa.md`: procedimiento, comparación por fronteras, preservación de runs e investigación de discrepancias.
- `templates/delivery-and-handoff.md`: registro copiable de reproducción, disponible en los nuevos workspaces.
- `templates/data-and-validation.md`: semántica de persistencia/lectura y referencia al registro.
- Playbooks de análisis y modelos: instrucciones de reproducción y referencias.
- Manual generado: recorrido, criterios y límites de automatización.
- Recursos empaquetados: sincronizados con las fuentes respectivas del OS.

No se modificaron contratos de estado, gates ni comandos. Los pilotos cerrados y el Foundry conservan sus artifacts.

## Verificación

Suite completa: `.venv/bin/python -m pytest` — **145 passed**, 4.58 s. Se ejecutó con permiso para localhost requerido por los tests existentes del proxy; los proveedores son simulados.

Ejemplo repetible desde el checkout:

```sh
PYTHONPATH=src .venv/bin/python docs/acos/validation/serialization-example.py
```

El ejemplo usa el compiler real para crear un workspace temporal y comprueba disponibilidad del template y sincronización de recursos. Después escribe un CSV con precisión explícita `.16g`, conserva IDs como strings y lee valores como floats. Los criterios previos son tolerancia numérica `rtol=1e-8`, `atol=1e-6` y selección exacta con `value > 0.3`.

| Recorrido | Valor | Selección | Comparación |
|---|---|---|---|
| Original: guardar y releer | 0.3 | Ningún ID | Referencia |
| Omitir la frontera y usar memoria | 0.30000000000000004 | 001 | Discrepancia, aunque cumple tolerancia numérica |
| Repetir escritura/lectura del recorrido original | 0.3 | Ningún ID | PASS |

La comprobación preservó el hash del CSV original y conservó ambos resultados en el destino temporal. Resultado guardado: [JSON del ejemplo](2026-10-09-serialization-example.json).

Costo API: **US$0**. Revisión nativa del alcance y coherencia documental; no constituye revisión independiente ni evaluación de eficacia de skills.

## Límites

Este ejemplo demuestra una regla sensible a representación con precisión explícita del writer. No implica que todo CSV cambie floats, no exige CSV para los proyectos ni reproduce el entrenamiento del piloto. Respetar el recorrido es necesario, pero no garantiza determinismo entre plataformas o bibliotecas.

`acos validate` mantiene sus checks: no ejecuta análisis ni reproduce pipelines automáticamente. La mejora se incluye al compilar proyectos nuevos desde este checkout; no actualiza snapshots existentes ni publica una release.

Siguiente mejora pendiente: revisar etiquetas, períodos y cutoffs junto con las cifras.
