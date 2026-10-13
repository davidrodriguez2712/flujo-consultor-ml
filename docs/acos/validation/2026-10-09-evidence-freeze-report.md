# Mejora del flujo: evidencia congelada y documentos vivos

Fecha: 2026-10-09. Alcance aprobado: pautas, templates y manual generado.

## Cambios

- El workflow distingue documentos vivos, evidencia congelada y aprobaciones externas al paquete; define rutas relativas, SHA-256, verificación y correcciones que conservan el original.
- El template de delivery registra integridad, historial y aceptación del manifest exacto. Incluye un registro separado de aprobación y referencias en el handoff.
- El manual generado explica el procedimiento y sus límites. El resolver incluye el template compartido en proyectos nuevos; los recursos empaquetados coinciden con las fuentes del OS.
- El OS principal referencia el procedimiento. No se modificaron los pilotos cerrados ni el Foundry.

## Verificación

1. Nuevo test del compiler: falló por ausencia del template de delivery antes del cambio; pasó tras incluirlo. Comprueba que el archivo se crea y figura en el manifest inicial.
2. Suite completa: `.venv/bin/python -m pytest` — **145 passed**, 4.22 s. La primera ejecución en sandbox obtuvo 142 passed y dos errores de permisos al abrir localhost; la ejecución con permiso para localhost pasó. Los proveedores son simulados; costo API US$0.
3. Ejemplo temporal con el compiler real y sin skills: generó manual, workflow y template. Se copió un plan vivo a una ruta histórica y se registraron hashes en un manifest separado. Tras actualizar el plan, STATE, MANUAL y TASKS, los hashes de la copia y del manifest se conservaron. Una alteración intencional posterior de la copia produjo discrepancia de hash.
4. Revisión nativa del alcance, referencias y coherencia entre fuentes y recursos. No constituye revisión independiente ni evaluación comparativa de skills.

Resultado del ejemplo: [JSON](2026-10-09-evidence-freeze-scenario.json). La ruta temporal es diagnóstica y puede desaparecer. El registro de aprobación del ejemplo quedó pendiente; no simula una aceptación humana real.

## Límites y siguientes mejoras

El ejemplo verifica el procedimiento ejecutado explícitamente con operaciones de archivos y hashes. ACOS no implementa freeze automático, inmutabilidad del filesystem ni verificación automática de paquetes históricos mediante `acos validate`. `.acos/manifest.yaml` mantiene su propósito de composición inicial.

Esta mejora se distribuye en los nuevos workspaces compilados desde este checkout actualizado. Los snapshots existentes conservan su versión; no se actualizan automáticamente. No hay publicación de release incluida en este trabajo.

Pendientes separados: documentar límites de serialización en la reproducción; revisar etiquetas, períodos y cutoffs junto con las cifras. No se crearon ni promovieron capacidades del Foundry.
