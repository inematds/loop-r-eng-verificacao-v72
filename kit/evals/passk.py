#!/usr/bin/env python3
"""passk.py — lê o TSV do rodar-evals.py (rodado com --k N) e separa sorte de confiabilidade.

pass@k  = fração de casos com PELO MENOS um acerto em k tentativas (o que um benchmark gosta de mostrar)
pass^k  = fração de casos que acertaram TODAS as k tentativas (o que um loop sem supervisão precisa)
Também mostra a taxa de cada rodada e o desvio entre elas: a mesma suíte, o mesmo agente, números diferentes.
Uso: python3 passk.py resultados.tsv
"""
import collections, statistics, sys

if len(sys.argv) != 2: sys.exit(__doc__)
casos, rodadas = collections.defaultdict(list), collections.defaultdict(list)
for l in open(sys.argv[1]).read().splitlines()[1:]:
    i, _, k, ok, _ = l.split("\t")
    casos[i].append(ok == "1"); rodadas[int(k)].append(ok == "1")
k = min(len(v) for v in casos.values())
taxa = [sum(v) / len(v) for _, v in sorted(rodadas.items())]
p1 = statistics.mean(taxa)
print(f"{len(casos)} casos × {k} tentativas")
print(f"taxa por tentativa: {p1:.0%}  (" + " · ".join(f"rodada {n + 1}: {t:.0%}" for n, t in enumerate(taxa))
      + (f"; desvio {statistics.pstdev(taxa) * 100:.0f} pontos)" if k > 1 else ")"))
print(f"pass@{k}: {sum(any(v) for v in casos.values()) / len(casos):.0%}  (ao menos 1 acerto)")
print(f"pass^{k}: {sum(all(v) for v in casos.values()) / len(casos):.0%}  (acertou todas)")
print(f"se fossem independentes, {p1:.0%}^{k} = {p1 ** k:.0%}")
instaveis = [i for i, v in sorted(casos.items()) if any(v) and not all(v)]
print("instáveis: " + (" ".join(instaveis) if instaveis else "nenhum"))
