#!/usr/bin/env python3
"""guarda-testes.py — congela o juiz (testes e tudo o que o pytest lê) e confere se alguém mexeu.

  congelar <repo>   grava o hash de cada arquivo protegido e o mínimo de testes, FORA do repo
  conferir <repo>   sai 0 só se nada protegido mudou, nada novo apareceu e os testes passam todos, sem pular

Variáveis: GUARDA_DIR (padrão ~/.local/state/guarda-testes/<repo>), TESTE (padrão "python3 -m pytest -q"),
PROTEGIDOS (padrão: tests/ *conftest.py pytest.ini pyproject.toml setup.cfg tox.ini).
"""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

if len(sys.argv) != 3 or sys.argv[1] not in ("congelar", "conferir"): sys.exit(__doc__)
acao, repo = sys.argv[1], Path(sys.argv[2]).resolve()
G = Path(os.environ.get("GUARDA_DIR") or Path.home() / ".local/state/guarda-testes" / repo.name)
TESTE = os.environ.get("TESTE", "python3 -m pytest -q")
PROT = os.environ.get("PROTEGIDOS", "tests/ *conftest.py pytest.ini pyproject.toml setup.cfg tox.ini").split()

def git(*a): return subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True).stdout.split("\n")
def protegidos():
    fs = git("ls-files", "--", *PROT) + git("ls-files", "--others", "--exclude-standard", "--", *PROT)
    return sorted({f for f in fs if f})
def sha(f): return hashlib.sha256((repo / f).read_bytes()).hexdigest()
def rodar(extra=""):
    p = subprocess.run(TESTE + extra, shell=True, cwd=repo, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or [""]

if acao == "congelar":
    G.mkdir(parents=True, exist_ok=True)
    _, ult = rodar(" --collect-only")
    n = int((re.search(r"(\d+) tests? collected", ult[0]) or [0, 0])[1])
    json.dump({"minimo": n, "hash": {f: sha(f) for f in protegidos()}}, open(G / "guarda.json", "w"), indent=1)
    sys.exit(print(f"congelado: {len(protegidos())} arquivos protegidos, mínimo de {n} testes → {G}/guarda.json"))

m = json.load(open(G / "guarda.json"))
erros = [f"APAGADO  {f}" for f in m["hash"] if not (repo / f).exists()]
erros += [f"MEXIDO   {f}" for f in m["hash"] if (repo / f).exists() and sha(f) != m["hash"][f]]
erros += [f"NOVO     {f}" for f in protegidos() if f not in m["hash"]]
rc, ult = rodar()
cont = {k: int(v) for v, k in re.findall(r"(\d+) (passed|failed|skipped|deselected|xfailed|xpassed|error)", ult[0])}
print(f"testes: {ult[0]} (código {rc}, mínimo {m['minimo']} passed)")
if rc != 0 or cont.get("passed", 0) < m["minimo"]: erros.append(f"POUCOS   {cont.get('passed', 0)} passed, mínimo {m['minimo']}")
erros += [f"PULADO   {cont[k]} {k}" for k in ("skipped", "deselected", "xfailed", "xpassed") if cont.get(k)]
print("\n".join(erros) + "\nGUARDA: REPROVADO" if erros else "GUARDA: OK")
sys.exit(1 if erros else 0)
