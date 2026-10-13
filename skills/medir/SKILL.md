---
name: medir
description: Mede quanto o Brain com o Graphify economiza de tokens nos seus projetos (benchmark do grafo e, se quiser, um teste A/B real com duas conversas) e registra o resultado no Status do projeto. Só faz sentido com o Graphify ligado. Use quando a pessoa disser /brain:medir, "quanto estou economizando", "vale a pena o graphify?", "medir tokens".
---

# Medir a economia de tokens

Roteador: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain.py"` (BRAIN).

## 0. Precisa do Graphify
`command -v graphify`. Não tem: explique em 2 linhas que é o Graphify que gera a economia grande (o Claude consulta um
mapa do código em vez de abrir arquivo por arquivo), que é **recomendado** e grátis, e ofereça ligar agora:
`pipx install graphifyy` (ou `pip install graphifyy`) e depois `/brain:conectar` na pasta do projeto. Sem Graphify, pare aqui.

## 1. Benchmark rápido (1 minuto, sem custo de token)
Para o projeto atual, ou para cada projeto ligado com `graphify-out/` (no máximo 5, os maiores primeiro):
`graphify benchmark "<pasta>/graphify-out/graph.json"`.
Mostre numa tabela: projeto · corpus (tokens, se o Claude lesse tudo) · custo médio por pergunta · redução (Nx).
Explique em uma linha: é o **teto** do ganho, porque compara com ler o projeto inteiro. Projeto grande e cheio de
documentos ganha muito; projeto pequeno ganha pouco.

## 2. Teste A/B real (opcional, a pessoa faz)
Para medir no uso de verdade:
1. Escolham juntos uma pergunta real sobre o projeto (ex.: "como funciona o fluxo de login?").
2. **Sessão A:** `/clear`, peça "responda sem usar graphify, lendo os arquivos normalmente" + a pergunta. No fim, `/context`.
3. **Sessão B:** `/clear`, peça "use só graphify query/explain, abra arquivo só se indispensável" + a mesma pergunta. `/context`.
4. Em cada sessão, diga quantos arquivos abriu. Ela compara os dois `/context` (e o `/usage`, se quiser).

## 3. Registrar
Acrescente em "Onde paramos" do `Status.md` do projeto uma linha datada: `AAAA-MM-DD: benchmark do Graphify ~Nx menos
tokens por pergunta (corpus ~X mil, ~Y mil por pergunta)` e o resultado do A/B, se houve. `BRAIN lint && BRAIN index`.
