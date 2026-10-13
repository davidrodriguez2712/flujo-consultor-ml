# detect-leakage 0.2.2 — cierre de pendientes sin costo

Fecha: 2026-10-13. Cero llamadas API nuevas en este cierre. Canonical 0.2.0 (SHA-256 `c2a2440477d9985489b71f4d8c50380ccd7985635d02eab330cfee0f7e5856c4`) y toda evidencia previa permanecen intactos. Madurez: **experimental**, sin promoción.

## 1. Resultado del L03 nativo con 0.2.2

`evaluations/foundry/2026-10-13-detect-leakage-v022/native-results-01/`. Runtime PASS, Skill nativa cargada, `check_inputs.py` ejecutado, reporte escrito. **Contrato mecánico FAIL: `report:word_limit`, 515 palabras frente al límite de 500** (final: 60/80). El coordinador se detuvo según lo previsto; no se reparó el reporte ni se reintentó.

Observación de contenido (lectura del autor, no revisión independiente): el reporte declara «No determinable», no afirma invalidez ni disponibilidad por la fecha de exportación, y expone ambas condiciones (confirmación y posible validez) más una acción provisional bajo el owner. Es el punto que L03 de 0.2.0 sobreafirmaba. Esto **no** convierte el resultado en PASS: el contrato falló y la revisión semántica independiente del output nativo sigue pendiente.

Coste real: US$0.004567405, 4 requests, todos HTTP200 y usage conocido. Acumulado del estudio: US$0.140197950 de US$0.15. Saldo: **US$0.00980205**; insuficiente para otra secuencia nativa completa (la reserva por request ya superó US$0.006 en L03). Pago detenido.

## 2. Compatibilidad formal del template

Causa: `quick_validate` solo admite `name, description, license, allowed-tools, metadata`; el template ponía `status/version/domain` en la raíz.

- Borrador `compat-template/detect-leakage/SKILL.md` (SHA-256 `054e676be6591243eb52675d1608f8f5a0614462685a21aacf8c15801661c4ea`): idéntico al borrador 0.2.2 salvo mover esos tres campos bajo `metadata:`. `quick_validate`: **Skill is valid!** (el original falla con «Unexpected key(s): domain, status, version»).
- Compilador (`src/acos/foundry.py`): ahora lee `status/version` también desde `metadata:`. La raíz tiene precedencia; el formato antiguo sigue funcionando. RED→GREEN con dos tests nuevos en `tests/test_foundry.py`. Suite completa: **264 PASS**. El borrador compatible se inventarió correctamente como `detect-leakage experimental 0.2.2`.
- No se migró ningún SKILL.md canónico, snapshot ni piloto: eso cambiaría hashes de manifests congelados y debe ser decisión de David.

Límite: se verificó con el validador de Codex, no con los demás runtimes.

## 3. Pendientes que no se pueden cerrar sin decisión humana

- Revisión semántica independiente del L03 nativo 0.2.2, y de si 515 palabras es fallo de contenido o solo de formato.
- Comparación nueva baseline vs. treatment, con escenarios menos guiados: requiere presupuesto adicional.
- Adjudicación humana antes de cualquier cambio de madurez.
