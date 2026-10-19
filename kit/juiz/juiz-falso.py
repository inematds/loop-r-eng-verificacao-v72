#!/usr/bin/env python3
"""juiz-falso.py — imita um juiz por modelo sem custo, com regras ingênuas de propósito.

R1: procura palavras de motivo ("porque", "para ", "evita", "antes", "perdiam", "corrige").
R2: sempre "sim" — este juiz não confere o diff (é o defeito que a calibração tem de pegar).
R3: "sim" se a mensagem tem mais de 25 caracteres.
"""
import json, re, sys

msg = sys.stdin.read().split("## MENSAGEM")[-1].strip()
r1 = re.search(r"porque|para |evita|antes|perdiam|corrige", msg, re.I)
print(json.dumps({"R1": "sim" if r1 else "nao", "R2": "sim", "R3": "sim" if len(msg) > 25 else "nao"}))
