---
name: conectar
description: Liga uma pasta (repositório ou não) a um projeto do Brain numa área da vida, para que toda conversa ali comece com o Status e as decisões. Opcionalmente liga o mapa do código (Graphify). Use quando a pessoa disser /brain:conectar, "conecta este projeto", "adiciona esta pasta ao Brain", ou quando o contexto avisar que a pasta não pertence a nenhum projeto e o trabalho vai durar.
---

# Conectar uma pasta

Roteador: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain.py"` (BRAIN). Sem cofre configurado: rode `/brain:setup`.

1. Leia no máximo 40 linhas de README, CLAUDE.md ou package.json da pasta para escrever o resumo (o que é, em uma frase).
2. Proponha a área (`BRAIN find` e o `INDEX.md` do cofre mostram as áreas) e o `id` (nome da pasta em minúsculas com hífen).
   Se a área não for óbvia, pergunte com AskUserQuestion. Área nova: `BRAIN area "<nome>" "<resumo>"`.
3. `BRAIN projeto <área> <id> "<pasta>" "<resumo>"`. Mesmo projeto em outra pasta (ex.: um segundo repo): use o mesmo
   `id`, que o caminho é acrescentado.
4. Se for repositório de código, **recomende o mapa do Graphify** (economiza muitos tokens: o Claude consulta o mapa em vez
   de abrir arquivo por arquivo) e pergunte se ela quer seguir com ele. Sim: `sh "${CLAUDE_PLUGIN_ROOT}/scripts/grafo.sh" ligar "<pasta>" <id>`
   (precisa do `graphify`: `pipx install graphifyy`). Ele não toca em arquivo versionado: o `graphify-out/` fica fora do git
   só nesta máquina, um hook de commit refaz o grafo e o repo entra no grafo global (perguntas entre projetos).
5. Anote stack e padrões que você já viu na seção "Stack e padrões" da nota do projeto (2 a 5 linhas).
6. `BRAIN lint && BRAIN index` e uma linha com o que mudou.
