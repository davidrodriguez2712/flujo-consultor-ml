# Encargo textual de auditoría

El cliente necesita una recomendación hoy sobre usar complaint_count para scoring. Audita solo el expediente suministrado. ¿Qué puedes concluir y qué evidencia permitiría cambiar esa conclusión?

Modo: guía textual, sin instalación/invocación nativa, filesystem, herramientas, entrenamiento o gates. Comprobaciones por lectura deben identificarse como tales.

Entrega un único documento Markdown de máximo250palabras por whitespace, incluidas metadata y todas las secciones. Frontmatter físico delimitado por --- con skill: detect-leakage, version de la guía seleccionada suministrada por el runner, fecha real suministrada, modo: guia_textual, estado e inputs (nombres de los tres archivos suministrados, sin hashes ni claims de ejecución). Cuerpo: Resumen, Hallazgos, Evidencia, Preguntas abiertas, Recomendaciones. El archivo inicia exactamente por una línea --- y cierra la metadata con otra línea ---, seguido por ## Resumen. Entregar sin fences exteriores ni texto externo al artifact. La guía aporta procedimiento, no evidencia de ejecución.

## Input: context.md
# Expediente disponible

Cada fila representa cliente al scoring 2025-06-01T00:00:00Z; target es cancelación en los30 días siguientes. La exportación se realizó 2025-08-01T00:00:00Z y contiene outcomes conocidos después del scoring para evaluación retrospectiva. Solo complaint_count se propone como feature. No hay código de construcción, fecha de disponibilidad, ventana de conteo, versión histórica ni split/preprocessing en el expediente. No se conoce si el conteo refleja el estado al scoring o al exportar. IDs, target y fechas son metadata, no features. La exportación no certifica cuándo existía la feature en producción.


## Input: dictionary.json
{
  "complaint_count": "Número de reclamos; ventana y disponibilidad no documentadas",
  "feature_available_at": null,
  "construction_code": null
}


## Input: observations.csv
customer_id,prediction_at,exported_at,complaint_count,cancelled_next_30d
U01,2025-06-01T00:00:00Z,2025-08-01T00:00:00Z,3,1
U02,2025-06-01T00:00:00Z,2025-08-01T00:00:00Z,0,0
U03,2025-06-01T00:00:00Z,2025-08-01T00:00:00Z,2,0

