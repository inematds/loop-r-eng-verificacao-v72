#!/usr/bin/env python3
"""conferir-goal.py — roda cada critério "comando → saída" de um goal.md e diz OK ou FALHOU.

Lê as linhas  - [ ] `comando` → `esperado`  (ou - [x]). O esperado pode ser:
  um trecho literal (palavra inteira na saída)  ·  vazio (saída vazia)  ·  código N (código de saída)
Critério sem comando entre crases não dá para conferir: conta como FALHOU.
Uso: python3 conferir-goal.py goal.md [--pasta DIR]   Sai com 0 só se tudo passar.
"""
import re, subprocess, sys

args = sys.argv[1:]
if not args: sys.exit(__doc__)
pasta = args[args.index("--pasta") + 1] if "--pasta" in args else "."
linhas = [l.strip() for l in open(args[0], encoding="utf-8") if re.match(r"\s*- \[[ xX]\]", l)]
falhas = 0
for l in linhas:
    m = re.match(r"- \[[ xX]\]\s*`([^`]+)`\s*(?:→|->)\s*`([^`]*)`", l)
    if not m:
        falhas += 1
        print(f"FALHOU  sem comando: {l[6:][:70]}")
        continue
    cmd, esperado = m.groups()
    p = subprocess.run(cmd, shell=True, cwd=pasta, capture_output=True, text=True, timeout=600)
    saida = (p.stdout + p.stderr).strip()
    if esperado == "vazio":
        ok = saida == ""
    elif re.fullmatch(r"código \d+", esperado):
        ok = p.returncode == int(esperado.split()[1])
    else:
        ok = re.search(r"(?<!\w)" + re.escape(esperado) + r"(?!\w)", saida) is not None
    print(f"{'OK    ' if ok else 'FALHOU'}  {cmd[:60]}  →  {esperado}")
    if not ok:
        falhas += 1
        print(f"        veio: {(saida.splitlines() or ['(vazio)'])[-1][:80]} (código {p.returncode})")
print("---")
print("PRONTO" if falhas == 0 else f"FALTAM {falhas}")
sys.exit(min(falhas, 100))
