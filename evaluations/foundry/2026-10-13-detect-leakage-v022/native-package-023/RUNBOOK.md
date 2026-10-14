# Diagnóstico nativo 0.2.3

L03 único, expected/case/workflow/transporte congelados idénticos a 0.2.2. Cambia solo la skill (0.2.3: un dato por sección). Cap 4096, reporte 500/final 80, sin retries. Techo acumulado US$0.18 autorizado por el usuario (+US$0.03); gasto previo US$0.14019795; proxy máximo de esta corrida US$0.02. Contrato mecánico fallido se conserva sin reparar. No promueve ni modifica canónico. config.budget_ceiling_usd 0.1 es cota del verificador, no fondos.

Desviación: el CLI local pasó de 2.1.296 a 2.1.299 tras la preparación; el guard de versión detuvo el primer lanzamiento sin gasto (native-launch-023.stderr). Se actualizó solo config.cli_version y se regeneró el manifest. La compatibilidad del transporte con 2.1.299 no estaba verificada previamente; la corrida no es comparable estrictamente con 0.2.2 (2.1.296).
