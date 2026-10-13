---
name: fechar
description: Fecha a sessão de trabalho no Brain atualizando o Status do projeto (o que foi feito, decisões, pendências, próximo passo, erros e soluções). Use quando a pessoa disser /brain:fechar, "fecha a sessão", "atualiza o status", "vou dar /clear", ou ao encerrar um trabalho relevante.
---

# Fechar a sessão

Roteador: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain.py"` (BRAIN). Cofre: `BRAIN onde`.
Projeto da pasta atual: o contexto "Brain · área" do início da sessão já mostra a nota e o `Status.md`. Se a pasta não
tem projeto, ofereça `/brain:conectar` primeiro.

Atualize `<projeto>/Status.md` e o `atualizado:` do frontmatter (AAAA-MM-DD):
- **Onde paramos:** o que foi feito, em até 5 tópicos datados, com os arquivos principais alterados. Resuma; não copie a conversa.
  Mantenha o histórico curto: funda tópicos antigos em uma linha quando passar de ~15.
- **Pendente:** o que ficou aberto. Tire o que foi resolvido.
- **Próximo passo:** o primeiro passo concreto da próxima sessão.
- **Erros e soluções:** erro que custou tempo e como foi resolvido (é o que evita repetir).
- Decisão nova com motivo: vira nota pelo formato do `/brain:decisao`, ligada a `[[status-<projeto>]]`.

Se mudou código e a pasta tem `graphify-out/`: `graphify update .` e `BRAIN mapa <projeto>`.
Fim: `BRAIN lint && BRAIN index` e uma linha com o que mudou. Nada de segredo, chave ou valor financeiro.
