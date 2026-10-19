#!/usr/bin/env bash
# portao.sh — o portão do loop: camadas baratas primeiro, modelo só no fim e só se elas passarem.
# Uso: portao.sh <repo> <portao.env>     (guarde o portao.env FORA do repo: o agente não pode editar o juiz)
# portao.env:  GOAL=...  GUARDA_DIR=...  ESCONDIDOS=...  EVAL_AGENTE=... EVAL_BASE=...  AVALIADOR_CMD=...
# Camada sem configuração é pulada e aparece como pulada. Sai 0 só com PORTÃO: APROVADO.
set -uo pipefail
K=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "${1:?uso: portao.sh <repo> <portao.env>}" && pwd)
# shellcheck disable=SC1090
source "${2:?falta o portao.env}"
L=${PORTAO_LOGS:-/tmp/portao}; mkdir -p "$L"; reprovou=(); linhas=()
camada() {  # nome, condição para rodar, comando
  if [ -z "$2" ]; then linhas+=("$(printf '%-10s pulada (sem configuração)' "$1")"); return; fi
  if bash -c "$3" > "$L/$1.log" 2>&1; then linhas+=("$(printf '%-10s OK' "$1")")
  else linhas+=("$(printf '%-10s REPROVADO  → %s' "$1" "$L/$1.log")"); reprovou+=("$1"); fi
}
camada criterios "${GOAL:-}" "python3 '$K/conferir-goal.py' '${GOAL:-}' --pasta '$repo'"
camada guarda "${GUARDA_DIR:-}" "GUARDA_DIR='${GUARDA_DIR:-}' python3 '$K/guarda-testes.py' conferir '$repo'"
camada atalhos "${ESCONDIDOS:-}" "python3 '$K/atalhos.py' '$repo' --escondidos '${ESCONDIDOS:-}'"
camada evals "${EVAL_BASE:-}" "python3 '$K/evals/rodar-evals.py' --agente '${EVAL_AGENTE:-}' --base '${EVAL_BASE:-}' --saida '$L/evals.tsv'"
if [ ${#reprovou[@]} -eq 0 ]; then
  camada avaliador "${AVALIADOR_CMD:-}" "AVALIADOR_CMD='${AVALIADOR_CMD:-}' REVIEW='$L/review.md' '$K/avaliar.sh' '$repo'"
else linhas+=("$(printf '%-10s pulada (camada barata já reprovou: não gaste cota)' avaliador)"); fi
printf '%s\n' "${linhas[@]}"
if [ ${#reprovou[@]} -eq 0 ]; then echo "PORTÃO: APROVADO"; exit 0; fi
echo "PORTÃO: REPROVADO em ${reprovou[*]}"; exit 1
