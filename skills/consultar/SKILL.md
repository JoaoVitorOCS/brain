---
name: consultar
description: Responde o que o Brain sabe sobre um assunto, projeto ou área, abrindo só as notas necessárias. Use quando a pessoa disser /brain:consultar, "o que o Brain sabe sobre...", "onde paramos em <projeto>", "o que decidimos sobre...".
---

# Consultar

Roteador: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain.py"` (BRAIN). Nunca leia o cofre inteiro.

1. `BRAIN find <termo>` (id, resumo e tags). Nada? Tente sinônimos e `grep -ril "<termo>" "$(BRAIN onde)/modulos" | head`.
2. `BRAIN show <id>` para a nota com os vizinhos em uma linha; `--hops 2` se precisar ir mais longe.
3. Área inteira: `BRAIN modulo <área>`.
4. Código (se houver Graphify): `graphify query "<pergunta>" --budget 1500` dentro da pasta do repo. Pergunta que cruza
   projetos: `graphify query "<pergunta>" --budget 1500 --graph ~/.graphify/global-graph.json` (grafo global).

Responda citando as notas (`[[id]]`) e diga quando o Brain **não** sabe. Não invente o que não está lá.
