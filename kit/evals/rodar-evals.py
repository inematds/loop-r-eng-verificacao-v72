#!/usr/bin/env python3
"""rodar-evals.py — roda o conjunto de ouro contra um agente e compara com a versão anterior.

Cada caso: prompt + "## ISSUE" + entrada vão pelo stdin do AGENTE; a 1ª linha de JSON da resposta é
conferida por código (campo a campo com "espera"). Grava um TSV: id, categoria, tentativa, ok, veio.
Uso: python3 rodar-evals.py --agente "CMD" --saida v2.tsv [--casos casos.jsonl] [--prompt prompt-triagem.md]
                            [--base v1.tsv] [--k 3]
Sai 1 se algum caso que passava em TODAS as tentativas da base agora falha (regressão).
"""
import argparse, collections, json, os, re, subprocess
from pathlib import Path

aqui = Path(__file__).parent
a = argparse.ArgumentParser()
a.add_argument("--agente", required=True); a.add_argument("--saida", required=True)
a.add_argument("--casos", default=aqui / "casos.jsonl"); a.add_argument("--prompt", default=aqui / "prompt-triagem.md")
a.add_argument("--base"); a.add_argument("--k", type=int, default=1)
o = a.parse_args()
prompt = Path(o.prompt).read_text()
casos = [json.loads(l) for l in open(o.casos) if l.strip()]
linhas, por_cat = [], collections.defaultdict(lambda: [0, 0])
for c in casos:
    for k in range(1, o.k + 1):
        p = subprocess.run(o.agente, shell=True, input=f"{prompt}\n## ISSUE\n{c['entrada']}\n", text=True,
                           capture_output=True, env=dict(os.environ, TENTATIVA=str(k)), timeout=300)
        m = re.search(r"\{.*?\}", p.stdout, re.S)
        try: veio = json.loads(m[0]) if m else {}
        except json.JSONDecodeError: veio = {}
        ok = all(veio.get(campo) == v for campo, v in c["espera"].items())
        linhas.append((c["id"], c["categoria"], k, int(ok), json.dumps(veio, ensure_ascii=False)))
        por_cat[c["categoria"]][0] += ok; por_cat[c["categoria"]][1] += 1
Path(o.saida).write_text("id\tcategoria\ttentativa\tok\tveio\n" + "".join("\t".join(map(str, l)) + "\n" for l in linhas))
for cat, (ac, n) in sorted(por_cat.items()): print(f"{cat:<10} {ac}/{n}")
total = sum(l[3] for l in linhas)
print(f"{'total':<10} {total}/{len(linhas)} ({100 * total / len(linhas):.0f}%)  → {o.saida}")
if not o.base: raise SystemExit(0)
def sempre_ok(arq):
    r = collections.defaultdict(list)
    for l in open(arq).read().splitlines()[1:]: i, _, _, ok, _ = l.split("\t"); r[i].append(ok == "1")
    return {i for i, v in r.items() if all(v)}
antes, agora = sempre_ok(o.base), sempre_ok(o.saida)
regressoes = sorted(antes - agora)
for i in sorted(agora - antes): print(f"MELHOROU  {i}")
for i in regressoes: print(f"REGRESSÃO {i} (passava em {Path(o.base).name})")
print("sem regressão" if not regressoes else f"{len(regressoes)} regressão(ões): não promova")
raise SystemExit(1 if regressoes else 0)
