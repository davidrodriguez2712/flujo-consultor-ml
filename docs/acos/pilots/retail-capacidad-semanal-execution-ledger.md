# Ledger — piloto integrado de forecasting semanal

Usuario autorizó el caso y ensayo: «aprobado». Proyecto creado con perfil canónico y compiler actual; composición consulting_core + data_analysis + forecast + executive_delivery. No skills instaladas.

1. Copia fuente pública normalizada verificada SHA-256; protocolo y plan congelados antes de observar resultados.
2. Cálculo/tests por TDD; 7 tests piloto pasan. Se corrigió un error de sintaxis antes del run real, sin modificación de protocolo.
3. Desarrollo: media de cuatro semanas seleccionada por WAPE 15,21% frente a 18,40% de baseline; final 18 semanas WAPE 13,15%, MAE 54,33, bias −37,92. No comparación de challenger en final.
4. Freeze PASS tras actualización de plan vivo/vistas; reproducción en copia externa al checkout PASS, 7 archivos iguales byte por byte; QA PASS con error deliberado en copia, 3 órdenes y exclusión de semana parcial.
5. Suite producto/piloto 153 passed. Trece comandos CLI verificaron integridad y gates NEEDS_REVIEW. Los 263 archivos del Handoff del piloto retail anterior conservaron sus hashes.
6. Preparados informe, recomendación y handoff; paquete congelado versión 01 con 70 archivos y hash del manifest `fdf2945c8935a3511a0766c3527fc9216609021ffa45eb5891f5c574c732e647`. Aprobación pendiente separada en handoff/human-approval.json.

Estado canónico: validation / IN_PROGRESS. Ninguna etapa completada ni gate PASS. Costo API US$0. No modificación del Foundry, publicación externa o uso operativo.

[Informe](../../../pilots/retail-capacidad-semanal-publico/PILOT_REPORT.md) · [Manifest](../../../pilots/retail-capacidad-semanal-publico/reports/package/evidence-manifest-01.json).

Límites: ejecución nativa guiada, sin control/treatment; datos previamente explorados; completitud y disponibilidad inmediata asumidas; reproducción mismo macOS/Python. No acredita eficacia de skills ni staffing real.

## Cierre aceptado

David: «Aprobado seguimos». Aceptación vinculada al manifest original fdf2945c8935a3511a0766c3527fc9216609021ffa45eb5891f5c574c732e647, sin cambiar sus 70 archivos. State COMPLETED; validation, delivery, handoff completos; 11 gates PASS, 13 comandos exit0. Sin pendientes dentro del ensayo ni nuevos costos. [Cierre](../../../pilots/retail-capacidad-semanal-publico/reports/closure/closure.md).
