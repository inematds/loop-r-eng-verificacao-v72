# Goal — slug (ensaio)

## Resultado
slug() transforma qualquer título em um endereço de página: minúsculas, sem acento, palavras unidas por hífen.

## Critérios de pronto
**Função**
- [ ] `python3 -m pytest -q tests/` → `3 passed`
- [ ] `python3 -c "from slug import slug; print(slug('Ação & Reação!'))"` → `acao-reacao`

**Regressão**
- [ ] `python3 -m pytest -q tests/ -rs` → `código 0`

**Limite**
- [ ] `git diff --stat HEAD -- tests/ pytest.ini` → `vazio`
- [ ] `git ls-files --others --exclude-standard -- '*conftest.py' tests/` → `vazio`
- [ ] o código fica limpo e bem documentado
