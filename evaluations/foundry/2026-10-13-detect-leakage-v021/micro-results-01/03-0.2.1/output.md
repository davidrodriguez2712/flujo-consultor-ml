---
skill: detect-leakage
version: 0.2.1
fecha: 2026-10-13
modo: guia_textual
estado: No determinable
inputs:
  - context.md
  - dictionary.json
  - observations.csv
---

## Resumen

No se puede recomendar hoy usar complaint_count para scoring. El expediente no acredita cuándo existía el conteo ni qué ventana cubría. La exportación de 2025-08-01 no fecha la feature. Recomendación provisional: no usarla en producción hasta verificar disponibilidad al 2025-06-01.

## Hallazgos

- **Componente:** complaint_count.
- **Conclusión:** No determinable.
- **Mecanismo demostrado o brecha:** brecha; sin fecha de disponibilidad, ventana de conteo ni código de construcción.
- **Fuente:** dictionary.json (feature_available_at y construction_code nulos); context.md.
- **Confianza en la conclusión:** baja-media; se basa en ausencia de evidencia.
- **Severidad del impacto potencial:** alta, por posible información posterior al scoring.
- **Acción:** reserva de uso bajo autoridad del owner hasta acreditar disponibilidad.

## Evidencia

- Lectura del expediente: el conteo no tiene fecha de corte documentada.
- Lectura de observations.csv: 3 filas, todas con prediction_at 2025-06-01 y exported_at 2025-08-01. Ningún valor se puede fechar por la exportación.
- Comprobación por lectura, no ejecutada: la correlación en la muestra (U01 con 3 reclamos y cancelación) no prueba leakage ni generalización.

## Preguntas abiertas

- ¿El conteo se calculó con datos hasta 2025-06-01 o se recalculó al exportar?
- ¿Cuál es la ventana del conteo?
- ¿Existe código de construcción y registro de disponibilidad en producción?

## Recomendaciones

- No usar complaint_count en scoring hasta obtener evidencia de disponibilidad al 2025-06-01.
- Solicitar código de construcción, ventana y fecha de corte al owner.
- Verificar con una extracción históricamente congelada, sin reconstruir sobre la exportación.
- Cambiar la conclusión solo si se demuestra que el conteo usa únicamente reclamos con timestamp anterior o igual a 2025-06-01 y que estaba disponible en producción en esa fecha.