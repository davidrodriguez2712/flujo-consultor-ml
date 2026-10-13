# Transferencia de pautas — preparación lista para revisión

David aprueba diseño de seis casos mediante «apruebo». Preparación y checks locales completados; **ninguna ejecución de modelos autorizada o realizada**.

## Cobertura

| ID | Engagement | Contraste |
|---|---|---|
| T01 | Churn/API | JSON puro, shortlist no causal. |
| T02 | Pricing/memo | Markdown humano, simulación sin causalidad. |
| T03 | Inventario/IDs | Reproducción fiel CSV → int → join. |
| T04 | Forecast/metodología | Reproducción y variante neta autorizada, versiones separadas. |
| T05 | Crédito/borrador | Freeze íntegro y plan vivo distinto; preparar task con dependencias. |
| T06 | Retención/lanzamiento | No enviar con approvals pendientes; preparación permitida. |

Seis casos sintéticos inéditos respecto a la evaluación previa; doce payloads baseline/treatment. Baseline es snapshot previo al ajuste; treatment es workflow actual. Solo se expone workflow, no templates/MANUAL: no se atribuirá efecto al compiler completo. Contratos de output son iguales dentro de cada par. Cuatro obligaciones y dos prohibiciones por case, reglas predefinidas para afirmaciones materiales adicionales y señal exploratoria.

## Verificación

`verify_preparation.py`: PASS. Reensambla doce payloads exclusivamente desde inputs públicos, verifica condiciones/diff, shortlist, márgenes, frontera CSV/int/join real, forecast bruto/neto, hashes de aprobación histórica y dependencias. Cinco contratos JSON y uno Markdown. Integridad de **253 archivos** históricos PASS.

Revisión local del autor; no independiente ni ciega. No outputs de agentes ni evidencia de eficacia. El autor conoce los fallos previos. No se ejecutó suite del producto porque solo se creó un paquete de evaluación; los checks de fixtures no son tests de eficacia.

**50 archivos congelados**, SHA-256 del manifest:

`ee7a0d2a15b46a82cf6a986f694d9023e9f2c3fb48825ef1560365f7d6453650`

[Paquete](../../../evaluations/os-workflow/2026-10-09-transfer-01/README.md) · [Protocolo](../../../evaluations/os-workflow/2026-10-09-transfer-01/protocol.md) · [Expected](../../../evaluations/os-workflow/2026-10-09-transfer-01/reviewer/case-index.json) · [Checks](../../../evaluations/os-workflow/2026-10-09-transfer-01/preparation-checks.json) · [Manifest](../../../evaluations/os-workflow/2026-10-09-transfer-01/evidence-manifest-01.json).

## Pendientes de ejecución

1. Revisión/aceptación concreta de paquete y expected.
2. Adaptar system prompt del transporte a contrato específico: hoy exige JSON y contradice T02. El envelope JSON del CLI no obliga al texto del modelo a ser JSON. Verificar checker Markdown, extracción de rutas y condiciones iguales; conservar snapshots históricos.
3. Fijar runtime/modelo/versión, aislamiento, límites y presupuesto en configuración nueva revisable; después autorización nueva de gasto. No transferir saldo de rondas anteriores.
4. Ejecutar sin retries automáticos y evaluar raw con rúbrica congelada, reportando formato/contenido/alcance por separado.

Cero calls y **US$0 adicional**. Acumulado de evaluación previa: US$0.02065453 estimados. Foundry, código del producto, transporte y evidencia histórica sin cambios. Ninguna promoción de madurez.
