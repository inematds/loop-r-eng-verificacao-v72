#!/usr/bin/env python3
"""juiz.py — juiz por modelo com rubrica sim/não: N repetições por artefato, vale a maioria.

Uso: python3 juiz.py [--rep 3] [--saida /tmp/juiz.csv] [--artefatos artefatos.jsonl] [--rubrica rubrica.md]
JUIZ_CMD = quem lê o pedido no stdin e responde JSON {"R1": "sim", ...}  (padrão: juiz-falso.py, sem custo)
A cada repetição a ordem dos critérios é embaralhada; critério sem unanimidade sai marcado "instável".
"""
import argparse, collections, json, os, random, re, subprocess
from pathlib import Path

aqui = Path(__file__).parent
a = argparse.ArgumentParser()
a.add_argument("--artefatos", default=aqui / "artefatos.jsonl"); a.add_argument("--rubrica", default=aqui / "rubrica.md")
a.add_argument("--rep", type=int, default=3); a.add_argument("--saida", default="/tmp/juiz.csv")
o = a.parse_args()
CMD = os.environ.get("JUIZ_CMD", f"python3 {aqui / 'juiz-falso.py'}")
crit = [[x.strip() for x in l.split("|")] for l in open(o.rubrica) if re.match(r"R\d+ \|", l)]
ids = [c[0] for c in crit]
saida = ["id," + ",".join(ids)]
erros = 0
for art in map(json.loads, filter(str.strip, open(o.artefatos))):
    votos = collections.defaultdict(list)
    for r in range(o.rep):
        ordem = random.Random(r).sample(crit, len(crit))
        pedido = ("Você é um juiz. Avalie a MENSAGEM contra cada critério. O DIFF resume o que de fato mudou.\n"
                  "Responda só uma linha de JSON com sim ou nao por critério, ex.: "
                  + json.dumps({c[0]: "sim" for c in crit}) + "\n\nCritérios:\n"
                  + "\n".join(f"{c[0]}: {c[1]}" for c in ordem)
                  + f"\n\n## DIFF\n{art['diff']}\n\n## MENSAGEM\n{art['texto']}\n")
        p = subprocess.run(CMD, shell=True, input=pedido, text=True, capture_output=True, timeout=300)
        m = re.search(r"\{.*?\}", p.stdout, re.S)
        try: resp = json.loads(m[0]) if m else {}
        except json.JSONDecodeError: resp = {}
        if not all(i in resp for i in ids):  # juiz fora do ar ou fora do formato: não vale como "nao"
            erros += 1
            print(f"{art['id']}  SEM RESPOSTA do juiz: {(p.stdout + p.stderr).strip()[:70]}")
            continue
        for i in ids: votos[i].append(str(resp[i]).lower().replace("não", "nao"))
    if not votos: continue
    final = {i: collections.Counter(v).most_common(1)[0][0] for i, v in votos.items()}
    instavel = [f"{i} {'×'.join(str(n) for n in collections.Counter(v).values())}" for i, v in votos.items() if len(set(v)) > 1]
    reprova = [c[0] for c in crit if "invari" in c[2] and final[c[0]] != "sim"]
    print(f"{art['id']}  " + " ".join(f"{i}={final[i]}" for i in ids)
          + (f"  instável: {', '.join(instavel)}" if instavel else "")
          + (f"  REPROVA ({', '.join(reprova)} invariável)" if reprova else ""))
    saida.append(art["id"] + "," + ",".join(final[i] for i in ids))
Path(o.saida).write_text("\n".join(saida) + "\n")
print(f"→ {o.saida}")
if erros: raise SystemExit(f"JUIZ FALHOU em {erros} chamada(s): artefato sem resposta ficou fora do CSV")
