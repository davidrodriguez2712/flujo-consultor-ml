# Task concreto — configuración02 lista

## Cambio aprobado y preparado

David aprobó preparar la nueva configuración. El único input modificado es el smoke: ahora incluye una plantilla literal que comienza por `## Estado` y coloca READY debajo. Los ocho casos, condiciones baseline/treatment, expected, rúbrica, prompt neutral, runtime y checker permanecen idénticos. La ronda01 fallida está intacta.

## Presupuesto y ejecución propuesta

Límite acumulado del estudio task-draft-01: **US$0.10**. Ronda01:US$0.000241 estimados por usage conocido. Máximo para ronda02: **US$0.099759**, un smoke + ocho respuestas, sin reintentos. La reserva conservadora puede detener la ronda si una solicitud no cabe; no se garantiza completar al máximo consumo.

La aprobación recibida cubre esta preparación. Ejecutar la ronda02 requiere aprobación contra su nuevo manifest; no se reutiliza la autorización ligada a configuration01. No se cargó la clave ni se creó proxy ni se llamó al proveedor en esta preparación.

## Checks locales

CLI2.1.296 y flags conformes; snapshots iguales al código activo. Preparación39, configuración01 de12 y ronda01 de17 archivos conservadas. El texto literal del smoke satisface checker0.2.0; este es un check de un texto del autor, no una respuesta del modelo. Compatibilidad real pendiente del nuevo smoke y eficacia del tratamiento NOT_EVALUATED. No se ejecutó otra suite de tests.

Configuración02 congelada:12 archivos, SHA256 de manifest `76ce8d316d09bd679e4efeea012792092c71640a134e7de326f4cc1226fc5a7e`. Control local sin anclaje externo. Producto y Foundry sin cambios; coste adicional de esta preparación US$0.

## Próximo paso

Aprobar la ejecución de configuration02 hastaUS$0.099759, manteniendo techo acumuladoUS$0.10. Entonces registrar aprobación vinculada al hash y ejecutar el schedule exacto. Ante fallo smoke/infraestructura/usage/presupuesto: detener sin retry. Conservar raw y revisar semánticamente los cuatro pares solo si se completan; no reparar respuestas ni modificar criterios para hacerlos pasar.
