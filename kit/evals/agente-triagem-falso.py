#!/usr/bin/env python3
"""agente-triagem-falso.py — imita o agente de triagem sem modelo (regras de palavra-chave).

TRIAGEM_VERSAO=1  regras originais
TRIAGEM_VERSAO=2  "melhoria": pergunta com ? vira dúvida antes de tudo (conserta um caso, quebra outro)
TRIAGEM_RUIDO=0.25  em 25% das tentativas inverte "urgente", sorteio fixo por caso + TENTATIVA (reproduzível)
"""
import hashlib, json, os, re, sys

texto = sys.stdin.read().split("## ISSUE")[-1].strip()
t = texto.lower()
versao = os.environ.get("TRIAGEM_VERSAO", "1")
if versao == "2" and t.endswith("?"):
    tipo = "duvida"
elif re.search(r"erro|não est|não encontra|desalinhad|consigo ver|ignora|não funciona", t):
    tipo = "bug"
elif re.search(r"poder |podem adicionar|seria ótimo", t):
    tipo = "pedido"
else:
    tipo = "duvida"
urgente = bool(re.search(r"\b500\b|pagamento|outros clientes|todos os usuários", t))
ruido = float(os.environ.get("TRIAGEM_RUIDO", "0"))
sorteio = int(hashlib.sha256((texto + os.environ.get("TENTATIVA", "1")).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
if sorteio < ruido:
    urgente = not urgente
print(json.dumps({"tipo": tipo, "urgente": urgente}))
