# Plantillas de datos y validación

Son formatos de trabajo para el proyecto, no templates de skills o evaluación del Foundry. Usar los apartados pertinentes; registrar versiones y decisiones que afecten resultados.

## Contrato de datos

Usar antes del análisis/modelo cuando varias fuentes, entidades, definiciones o controles puedan cambiar la conclusión. En un dataset simple y conocido, registrar la fuente y definiciones en el brief puede bastar.

```markdown
# Data contract — [dataset/proceso]

- Proyecto / owner de datos:
- Fuente canónica y contacto:
- Fecha, zona horaria y método de extracción:
- Ruta/tabla/versionado y hash del snapshot cuando aplique:
- Formato, writer/reader, opciones y esquema de lectura:
- Precisión, encoding, nulos y orden material en persistencia/lectura:
- Clasificación/retención/restricciones:

## Semántica
- Grain (una fila representa):
- Primary key(s):
- Entity key(s):
- Timestamp/event time y zona horaria:
- Ventana de cobertura:
- Definiciones críticas y owner que las confirma:
- Joins y cardinalidad esperada:

## Disponibilidad y calidad
- Campos necesarios y disponibilidad al momento de decisión:
- Nulos/duplicados/rangos/valores tardíos:
- Cohortes maduras o ventana de resultado:
- Exclusiones y razones:
- Checks, umbral, resultado y fecha:

## Cambios y aceptación
- Supuestos/limitaciones:
- Cambios de esquema conocidos:
- Evidencia asociada (SQL, notebook, query/job):
- Aceptado por / fecha o pendientes:
```

## Registro de validación

Usar cuando una afirmación depende de un cálculo, experimento o modelo cuyo método y límites necesitan revisión. El registro de validación de proyecto no es una `evaluation` de skill del Foundry.

```markdown
# Validation record — [claim/model/experiment]

- Proyecto / responsable / reviewer:
- Versión de datos, código, modelo y fecha:
- Pregunta de decisión:
- Método y criterio definido antes de observar resultados:
- Comparador/baseline:
- Población, unidad y período:
- Split/diseño y justificación:
- Registro de reproducción: entorno, comandos, fronteras de serialización y criterios de comparación:

## Checks pertinentes
- [ ] Calidad/definiciones y denominador
- [ ] Cohorte/ventana madura
- [ ] Leakage y disponibilidad temporal de features
- [ ] Leakage entre entidad/grupos, si aplica
- [ ] Métrica alineada al uso y costo de error
- [ ] Segmentos, estabilidad y casos fuera de soporte
- [ ] Incertidumbre/significancia y tamaño de muestra
- [ ] Umbral/criterio de despliegue o decisión

## Resultado y límites
- Evidencia/resultados con unidades:
- Resultado de cada check y referencia:
- Hallazgos negativos/contradictorios:
- Limitaciones y supuestos:
- Qué conclusión está respaldada:
- Qué conclusión no está respaldada:
- Decisión humana / owner / fecha:
- Revalidación necesaria si:
```

Documentar el recorrido realmente ejecutado, incluidas escrituras y lecturas antes de calcular o entrenar. El registro copiable está en [`delivery-and-handoff.md`](delivery-and-handoff.md). No declarar resultados reproducidos solo porque los inputs estén dentro de tolerancia.
