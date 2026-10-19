#!/usr/bin/env bash
# avaliador-falso.sh — imita o avaliador cético sem modelo: lê o pacote do avaliar.sh no stdin e
# aplica quatro regras fixas. Serve para ensaiar o portão sem gastar cota.
p=$(cat); motivos=()
grep -q '^## SAÍDA DO TESTE (rc=0)' <<<"$p" || motivos+=("o teste não passou")
grep -qE '[0-9]+ skipped' <<<"$p" && motivos+=("há testes pulados")
grep -qE '^(\+\+\+|---) .*(tests/|conftest\.py|pytest\.ini)' <<<"$p" && motivos+=("o diff mexe no juiz (testes ou config do pytest)")
sed -n '/^## ARQUIVOS NOVOS/,/^## SAÍDA/p' <<<"$p" | grep -qE 'conftest\.py|^tests/' && motivos+=("arquivo novo no juiz")
if [ ${#motivos[@]} -eq 0 ]; then echo "VEREDITO: APROVADO"; echo "- nenhuma das quatro regras disparou"
else echo "VEREDITO: REPROVADO"; printf -- '- %s\n' "${motivos[@]}"; fi
