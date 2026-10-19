#!/usr/bin/env python3
"""calibrar.py — compara o juiz com os rótulos de uma pessoa, critério por critério.

Uso: python3 calibrar.py humano.csv /tmp/juiz.csv [--min 0.8] [--kappa 0.6]
Concordância < 80% ou kappa de Cohen < 0,6 num critério = reescreva o critério ou troque o juiz.
Sai 0 só se todos os critérios passarem (JUIZ CALIBRADO).
"""
import csv, sys

args = sys.argv[1:]
if len(args) < 2: sys.exit(__doc__)
lim = float(args[args.index("--min") + 1]) if "--min" in args else 0.8
lk = float(args[args.index("--kappa") + 1]) if "--kappa" in args else 0.6
h = {r["id"]: r for r in csv.DictReader(open(args[0]))}
j = {r["id"]: r for r in csv.DictReader(open(args[1]))}
ids = sorted(h.keys() & j.keys())
ruins = []
print(f"{len(ids)} artefatos rotulados pelos dois")
for c in [k for k in next(iter(h.values())) if k != "id"]:
    pares = [(h[i][c], j[i][c]) for i in ids]
    po = sum(a == b for a, b in pares) / len(pares)
    ps = [sum(x == "sim" for x in col) / len(pares) for col in zip(*pares)]
    pe = ps[0] * ps[1] + (1 - ps[0]) * (1 - ps[1])
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    ok = po >= lim and kappa >= lk
    difs = " ".join(i for i, (a, b) in zip(ids, pares) if a != b)
    print(f"{c}  concordância {po:.0%}  kappa {kappa:.2f}  {'ok' if ok else 'REESCREVA ou troque o juiz'}"
          + (f"  (discorda em {difs})" if difs else ""))
    if not ok: ruins.append(c)
print("JUIZ CALIBRADO" if not ruins else f"JUIZ DESCALIBRADO em {', '.join(ruins)}: não use para aprovar")
sys.exit(1 if ruins else 0)
