#!/usr/bin/env bash
# avaliar.sh — avaliador SEPARADO e cético. Não lê o relato do agente: roda o teste ele mesmo e
# entrega diff + saída do teste a outro avaliador (sem ferramentas, só leitura) com o prompt cético.
# Uso: avaliar.sh <repo>
#   TESTE          comando de teste (padrão: python3 -m pytest -q)
#   AVALIADOR_CMD  quem lê o pacote no stdin e responde "VEREDITO: ..." (padrão: avaliador-falso.sh, sem custo)
#   REVIEW         onde gravar a revisão (padrão: /tmp/avaliar-review.md, fora do repo)
set -uo pipefail
K=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "${1:?uso: avaliar.sh <repo>}" && pwd)
TESTE=${TESTE:-python3 -m pytest -q}
AVALIADOR_CMD=${AVALIADOR_CMD:-$K/avaliador-falso.sh}
REVIEW=${REVIEW:-/tmp/avaliar-review.md}
cd "$repo"
saida=$(bash -c "$TESTE" 2>&1); rc=$?
echo "teste rodado pelo avaliador: $(echo "$saida" | tail -1) (rc=$rc)"
{ cat "$K/prompt-avaliador.md"
  echo; echo "## DIFF (git diff HEAD)"; git diff HEAD
  echo; echo "## ARQUIVOS NOVOS"; git ls-files --others --exclude-standard
  echo; echo "## SAÍDA DO TESTE (rc=$rc)"; echo "$saida" | tail -25
} | bash -c "$AVALIADOR_CMD" > "$REVIEW" 2>&1
v=$(grep -m1 -oE '^VEREDITO: (APROVADO|REPROVADO)' "$REVIEW" | cut -d' ' -f2)
echo "avaliador: ${v:-SEM VEREDITO} (revisão em $REVIEW)"
if [ "$rc" -eq 0 ] && [ "$v" = APROVADO ]; then echo "RESULTADO: APROVADO"; exit 0; fi
echo "RESULTADO: REPROVADO"; exit 1
