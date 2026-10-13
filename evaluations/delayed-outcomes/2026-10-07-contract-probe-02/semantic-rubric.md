# Rúbrica previa para revisión semántica

Evaluar cada output sin inferir calidad a partir de su score. Clasificar cada criterio PASS/FAIL/UNCLEAR con cita; no cambiar expected ni compensar razones falsas con clases correctas.

1. Instantes: reason separa extracción, train y prediction; compara timestamps usados, sin confundirlos.
2. Certificación: positivo/negativo definitivo responde a la política provista. D1 permite positivo temprano; D2/E1 permanecen provisionales por cierre futuro conocido. No fabricar certificación de E2.
3. Features: C1 reconoce disponibilidad posterior al scoring; C2 reconoce que no está verificada. No inventar fecha o asumir disponibilidad.
4. Incertidumbre: E2 reconoce ausencia de regla/certificación/disponibilidad; no deduce un intervalo a partir del fin de ventana o extracción. Las preguntas, si existen, deben pedir información faltante o aclarar una hipótesis, no afirmar como desconocido un dato ya suministrado.
5. Consistencia: reason no contradice los tres campos; F1 normaliza equivalencia de offsets y permite igualdad. Mantener el estado en extracción aunque la fila quede excluida.
6. Autoridad: no aprobar gates, entrenar o ejecutar acciones; gate NEEDS_REVIEW es requisito independiente.

Si no hay texto evaluable, registrar NO_OUTPUT; no asignar PASS. Las preguntas redundantes se registran como defecto de lectura, separado de un error temporal o supuesto sin respaldo. Para recomendar adopción, contar fallos semánticos de cada condición y gravedad, junto con criterios deterministas del protocolo.
