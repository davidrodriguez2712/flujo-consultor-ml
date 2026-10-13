Redacta el borrador de la próxima tarea para preparar una evaluación retrospectiva del forecast de ventas semanales. El owner lo revisará antes de decidir su ejecución.

## Contrato de salida

Un único objeto JSON, sin fences ni texto externo, con status (READY, MUST_CORRECT o NOT_DETERMINABLE), findings (lista de objetos con statement y evidence_paths), proposed_actions (lista de strings), next_step (string), limitations (lista de strings). Se permiten campos adicionales JSON; no se exige nombre particular para ellos. evidence_paths debe corresponder exactamente a claves de los artifacts incluidos.
