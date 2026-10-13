---
name: revisar
description: Revisa o diário automático do Brain (uma nota por sessão em inbox/sessoes/) e decide, com o ok da pessoa, o que vira Status, Decisão ou nota, e o que se descarta. Use quando a pessoa disser /brain:revisar, "revisar sessões", "o que ficou pendente no diário", ou quando a abertura avisar sessões aguardando revisão.
---

# Revisar o diário

Roteador: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain.py"` (BRAIN). Cofre: `BRAIN onde` (chame de COFRE).
Os hooks gravam cada sessão em `COFRE/inbox/sessoes/<data>-<projeto>-<id>.md` com `status: pendente` (pedidos, ações,
arquivos, pesquisas, commits). Nada entra no Brain sem esta revisão.

1. `BRAIN pendentes <projeto>` para o projeto atual, ou `BRAIN pendentes` para todos se a pessoa pedir. Pule a sessão
   que está aberta agora.
2. Antes de propor, veja o que o Brain **já** registra (Status, Decisões, nota do projeto): muita coisa foi gravada
   durante a própria sessão. Proponha só o que falta.
3. Para cada sessão, em poucas linhas, classifique cada item:
   - **Status:** feito e próximo passo → `<projeto>/Status.md`;
   - **Decisão:** escolha com motivo → `<projeto>/Decisoes/` (formato do `/brain:decisao`);
   - **Conhecimento:** fato durável, padrão, preferência → nota na área certa (formato do `/brain:lembrar`);
   - **Nada:** conversa operacional, tentativa descartada.
4. Espere o ok (ela pode cortar ou ajustar itens). Aplique só o aprovado.
5. No frontmatter da sessão, troque `status: pendente` por `status: revisado` (ou `descartado`); troque também o
   "status da revisão" do corpo e substitua os checkboxes da seção "Revisão" por uma linha com a data e o que foi feito.
6. `BRAIN lint && BRAIN index` e uma linha dizendo o que mudou.

Pasta sem projeto no Brain acumulando sessões: sugira `/brain:conectar`. Nunca grave segredo, chave ou valor financeiro.
