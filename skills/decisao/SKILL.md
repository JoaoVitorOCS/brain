---
name: decisao
description: Registra uma decisão de arquitetura ou de rumo no Brain, com contexto, opções, motivo e como desfazer. Use quando a pessoa disser /brain:decisao, "registra essa decisão", "decidimos que...", ou quando uma escolha relevante acabou de ser feita na conversa.
---

# Registrar decisão

Roteador: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain.py"` (BRAIN). Cofre: `BRAIN onde`. Projeto: o da pasta atual
(contexto do início da sessão); sem projeto, pergunte em qual projeto ou área registrar.

Crie `<projeto>/Decisoes/AAAA-MM-DD <título curto>.md`:

```markdown
---
tipo: decisao
data: AAAA-MM-DD
projeto: "[[<projeto>]]"
resumo: <a decisão em uma linha>
motivo: <o porquê em uma linha>
tags: [decisao]
---
# <título>

**Contexto:** o problema e o que levou à escolha.
**Opções consideradas:** (a) ... (b) ... com o prós e contras de cada uma em uma linha.
**Decisão:** o que foi escolhido.
**Motivo:** por quê.
**Afeta:** arquivos, módulos ou nós do grafo (se houver `graphify-out/`: `graphify explain "<nó>"`, `graphify affected "<nó>"`).
**Como desfazer:** o caminho de volta.

Ligado a [[status-<projeto>]].
```

Acrescente a decisão em uma linha no `Status.md` do projeto. Fim: `BRAIN lint && BRAIN index`.
