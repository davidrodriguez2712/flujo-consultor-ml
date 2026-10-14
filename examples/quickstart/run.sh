#!/usr/bin/env bash
# Recorrido e2e sin interacción manual: perfil -> workspace -> status/next -> gate framing BLOQUEADO -> completar -> PASS.
# Uso: bash examples/quickstart/run.sh [carpeta-destino]   (requiere `acos` en PATH)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-$(mktemp -d)}"
mkdir -p "$DEST" && cd "$DEST"

echo "== 1. Inicializar workspace desde un perfil (respuestas: sin guardar Foundry, confirmar propuesta)"
printf '\ns\ns\ns\ns\ns\n' | acos init demo-fraude --profile-file "$HERE/fraud-profile.yaml" >/dev/null
cd demo-fraude

echo "== 2. Estado y siguiente paso"
acos status | head -12
acos next | head -9

echo "== 3. Gate framing sin completar -> BLOCKED (código 4)"
acos validate --gate framing || echo "código de salida: $?"

echo "== 4. Completar framing/framing.yaml y registrar la revisión humana"
cat > framing/framing.yaml <<'Y'
decision: Priorizar inspecciones de fraude eléctrico
owner: Gerencia de Pérdidas No Técnicas (ficticia)
metric: Recuperación de energía por inspección
unit: kWh recuperados por inspección
horizon: 90 días
Y
HASH="$(grep profile_sha256 .acos/manifest.yaml | awk '{print $2}')"
python3 - "$HASH" <<'Y'
import sys
p = '.acos/state.yaml'
t = open(p).read().replace('gate_reviews: {}', f'''gate_reviews:
  framing:
    decision: PASS
    reviewer: David
    evidence:
      - framing/framing.yaml
    profile_sha256: {sys.argv[1]}''')
open(p, 'w').write(t)
Y

echo "== 5. Gate framing -> PASS"
acos validate --gate framing
echo "Workspace: $DEST/demo-fraude"
