# Paquete de evaluación menos guiada — preparación

**Estado:** preparado para revisión. Seis cases nuevos, doce payloads, cero llamadas de modelos y US$0 de API. No hay resultados de eficacia.

- [Protocolo](protocol.md): diseño, límites y requisitos pendientes para ejecutar.
- [Registro de preparación](preparation.json): configuración/budget aún sin fijar; no ejecución autorizada.
- [Índice privado de cases](reviewer/case-index.json) y [expected](reviewer/expected/): solo reviewer/checker, nunca payload.
- [Pautas baseline](conditions/baseline/workflow.md) y [treatment](conditions/treatment/workflow.md).
- `agent_inputs/`: contexto y artifacts de cada expediente hipotético.
- `payloads/`: entradas completas y separadas por condición; ningún expected incluido.

## Verificación local

Desde este directorio, usar Python 3.11+ (verificado Python 3.13.2):

```sh
python verify_preparation.py
```

El script verifica estructura, identidad del resto de las pautas, armado de payloads, hashes/referencias de fixtures, efectos del writer/reader, semántica de JSON y 24 órdenes de cada tabla de entregas. Si existe un manifest congelado, verifica también sus hashes. No llama modelos ni puntúa sus respuestas.

La separación de carpetas no acredita aislamiento del runtime: para ejecutar habrá que enviar solo el payload a una sesión nueva con herramientas deshabilitadas y verificar su configuración. No usar el contexto del autor para presentar una respuesta como evaluación independiente.

## Próximo paso

Revisar y aceptar o corregir el paquete; después definir runtime/modelo, transporte/checker y presupuesto. Mantener aprobación/configuración y futuros runs fuera del manifest congelado. La necesidad del artefacto determina si hace falta conocimiento, template, skill o agent; esta preparación no justifica promoción del Foundry.
