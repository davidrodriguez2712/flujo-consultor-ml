# Ajustes de formato, reproducción y continuidad

## Estado

**Implementados y verificados localmente.** David aprobó el diseño acotado mediante «apruebo». La comprobación de generación y regresiones pasó; la eficacia de agentes con estas nuevas instrucciones todavía no está evaluada.

## Cambios

### Contrato de salida

El contrato específico de la tarea controla consumidor, formato, campos/tipos y texto adicional. Un pedido de JSON puro implica un único objeto sin fences ni explicaciones externas; los ejemplos Markdown del OS no alteran ese contrato. Formato y contenido se revisan por separado. Outputs inválidos se conservan y cualquier corrección se registra como versión nueva autorizada. El formato humano sigue disponible para las tareas que lo acuerdan.

Template de tarea incorpora esos campos y distingue propuesta/revisión/ejecución/aceptación humana. El compiler ahora instala `templates/project-and-task.md` en la composición básica y registra su hash inicial en el manifest, conforme al ownership humano de templates.

### Reproducción fiel

El workflow, el registro de reproducción y el manual separan reproducir, diagnosticar y corregir el método. Primero repetir las fronteras originales, incluso cuando el redondeo parezca cuestionable. La selección sobre fuente cruda no es automáticamente canónica cuando el contrato consume un valor persistido.

Para `14.96 -> writer .1f -> reader 15.0 -> umbral >=15.0`, repetir fielmente debe conservar la selección original. La pregunta sobre si ese redondeo conviene al negocio se registra como propuesta metodológica separada. Ante una reproducción que omite writer/reader, repetir los originales en un destino nuevo autorizado; conservar ambos runs y los intentos fallidos.

### Continuidad de planes vivos

Dentro del mandato de revisión/propuesta, preparar la siguiente tarea y declarar sus dependencias pendientes. Una copia histórica íntegra conserva su alcance aunque el plan vivo cambie. La diferencia por sí sola no invalida el paquete ni exige congelar cada propuesta. Los bloqueos se aplican a las acciones dependientes de permisos, scope o gates todavía no acordados. El agente sigue sin aceptar gates ni transferir aprobaciones a nuevo alcance.

## Archivos

- [Workflow](../../../workflow/execution-and-qa.md).
- [Template de tarea](../../../templates/project-and-task.md).
- [Registro de reproducción](../../../templates/delivery-and-handoff.md).
- Manual generado en `src/acos/render.py` y selección del template en `src/acos/resolver.py`.
- Copias instalables correspondientes bajo `src/acos/resources/os/`.

No se añadieron comandos ni campos al schema de profile/state. Las instrucciones se distribuyen a proyectos nuevos; los paquetes históricos conservan sus versiones.

## Verificación

- Test de instalación del contrato observado RED porque faltaba el archivo; GREEN después de incluirlo en el resolver. Verifica copia canónica y `initial_sha256`, no frases de las instrucciones.
- Suite completa: **165 passed**, sin failures ni skips.
- Proyecto temporal compilado con recursos actualizados. `acos status` y `acos next`: exit0, integrityOK. `acos validate`: exit3, NEEDS_REVIEW esperado; no implica aceptación automática.
- Wheel construido localmente sin descarga de dependencias; recursos seleccionados coinciden con copias canónicas. No publicación de release.
- Source/bundle idénticos; templates generados idénticos. El workflow generado modifica solo un enlace opcional de UI no seleccionado mediante el renderer existente, revisado por separado.
- Integridad de **241 archivos** anteriores PASS: preparación, ambas configuraciones y rondas de evaluación, paquete aprobado del piloto.
- Revisión local de las tres situaciones: coherencia de pautas/template/manual. Es revisión del autor, **no simulación independiente de un agente ni prueba de eficacia**.

El probe inicial usó una ruta temporal bajo `/var`, rechazada por ser symlink; se corrigió el probe usando `/private/var` resuelto, conservando la protección del compiler. Se corrigieron también el entorno de importación local y la expectativa del campo de hash del test (`initial_sha256`).

[Checks de generación](../../../artifacts/os-workflow-refinement-2026-10-09/generation-checks.json) · [Revisión y límites](../../../artifacts/os-workflow-refinement-2026-10-09/local-review.json) · [Ejemplo de MANUAL generado](../../../artifacts/os-workflow-refinement-2026-10-09/generated-MANUAL.md).

Doce archivos de snapshots/evidencia congelados en [manifest del cambio](../../../artifacts/os-workflow-refinement-2026-10-09/change-manifest-01.json), SHA-256 `a29f377aaf26a4d92f74bf953709492477de9f3e41799a167c6244423a108088`.

## Consumo y siguiente paso

**US$0 adicionales**, cero llamadas de modelos. Coste acumulado de la evaluación anterior sigue en US$0.02065453. Foundry y evidencia histórica intactos; ninguna promoción de madurez.

Siguiente paso: diseñar un paquete de transferencia con casos inéditos para estas tres pautas, fijando criterios y condiciones antes de respuestas. Después revisar configuración y presupuesto de ejecución. El gasto restante de la ronda anterior no autoriza por sí solo nuevas llamadas. Estas mejoras ya están implementadas; su eficacia sigue pendiente de evaluación.
