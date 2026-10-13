# Cierre — riesgo de crédito sintético

David aprobó Handoff y cierre mediante «aprobar», después de revisar el paquete presentado. Estado canónico COMPLETED; siete etapas y doce gates aprobados, sin trabajo obligatorio restante del laboratorio.

## Resultado conservado

Baseline final: Brier 0.102487 frente a 0.116530, ROC-AUC 0.752283 en 447 concedidas maduras. Mejora puntual sintética; decisión sobre todas las solicitudes parcialmente respondida. Top-100 global con coverage 22–26%, sin métricas globales identificadas. No evidencia causal de revisión o ahorro, ni calibración certificada.

Reproducción en otra carpeta del mismo macOS/Python: seis archivos de datos, seis JSON de development y siete JSON finales idénticos. Metadata coincide salvo timestamp. Sin llamadas adicionales a APIs.

## Evidencia y continuidad

Aprobación en `evidence/approvals/2026-10-08-handoff.md`. Estado/vistas y comprobación CLI en `handoff/handoff-manifest-02-closed.json` y `reports/handoff/closure-verification.json`. El manifest de Handoff preparado y los manifests de etapas anteriores permanecen intactos; sus estados pendientes son históricos.

Runbook para replay y `handoff/next_steps.md` para futuras iniciativas. Windows nativo sigue pendiente. Las capacidades permanecen experimental; este cierre no modifica el Foundry ni autoriza uso crediticio real.
