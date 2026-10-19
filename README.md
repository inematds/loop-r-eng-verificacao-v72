# Verificação e Evals — Formação LOOP-R Engenharia (curso 1 de 6)

Curso aberto e gratuito do INEMA.CLUB no formato INEMA Learning v7.2, em português, inglês e espanhol:
**https://inematds.github.io/loop-r-eng-verificacao-v72/** · [EN](https://inematds.github.io/loop-r-eng-verificacao-v72/en/) · [ES](https://inematds.github.io/loop-r-eng-verificacao-v72/es/)

Oito aulas para quem já usa Claude Code ou Codex no terminal: avaliador separado e cético, critério comando → saída e o avaliador do `/goal`, testes congelados com guarda, detecção de atalho (reward hacking), conjunto de ouro com regressão, juiz por modelo calibrado, pass@k × pass^k e um portão em camadas para o seu loop.

## O kit (`kit/`)

Scripts pequenos (python3 + pytest + git). Todos têm um ensaio sem custo (agente, avaliador e juiz falsos) e um caminho real por variável (`AVALIADOR_CMD`, `--agente`, `JUIZ_CMD`) que usa `claude -p --tools ""` ou `codex exec -s read-only` pela sua assinatura.

| arquivo | aula | o que faz |
|---|---|---|
| `ensaio.sh`, `agente-falso.sh` | todas | projeto de teste com 3 testes visíveis e 3 escondidos; agente falso (bom, mente, apaga, conftest, chumba) |
| `avaliar.sh`, `prompt-avaliador.md`, `avaliador-falso.sh` | 1 | avaliador separado: roda o teste por fora e manda diff + saída a outro avaliador |
| `conferir-goal.py`, `goal-ensaio.md` | 2 | roda cada critério `comando` → `saída` do goal.md |
| `guarda-testes.py` | 3 | congela testes, conftest e config do pytest fora do repo e confere |
| `atalhos.py` | 4 | testes escondidos + sinais de atalho no diff |
| `evals/` | 5, 7 | conjunto de ouro, runner com regressão, pass@k e pass^k |
| `juiz/` | 6 | rubrica sim/não, juiz com repetições, calibração (concordância e kappa) |
| `portao.sh` | 8 | as camadas em fila, baratas primeiro |

```bash
git clone https://github.com/inematds/loop-r-eng-verificacao-v72 ~/projetos/loop-r-eng-verificacao-v72
K=~/projetos/loop-r-eng-verificacao-v72/kit && bash $K/ensaio.sh
```

## Gerar o site

Conteúdo em `conteudo/<idioma>/` (JSON). O HTML é gerado: `python3 gerar.py && python3 validar.py --links` (e `--lang en|es`). Não edite o HTML à mão.
