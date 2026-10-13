# Brain · cérebro externo para o Claude Code

O Claude Code esquece tudo quando a conversa acaba. O Brain é uma pasta de notas em markdown, no seu computador, que dá
memória a ele: **toda conversa nova num projeto já começa sabendo onde você parou**, o que está pendente e o que foi
decidido, e cada sessão vira um diário que você revisa.

```
Brain/                         (abre no Obsidian, se você quiser)
  Inicio.md  INDEX.md          página inicial · mapa gerado que entra no contexto
  modulos/
    pessoal/ trabalho/ projetos/ ...      uma pasta por área da sua vida
      <projeto>/  <projeto>.md  Status.md  Decisoes/  Mapa/
  referencias/  inbox/sessoes/            fontes externas · diário automático de cada sessão
```

## Instalar
Precisa do [Claude Code](https://claude.com/claude-code) e do Python 3.9+ (só a biblioteca padrão). No Claude Code:
```
/plugin install brain --marketplace JoaoVitorOCS/brain
```
Esse comando adiciona o marketplace **e** instala o plugin (só o `/plugin marketplace add` não instala nada).
Depois, numa conversa nova (ou após `/reload-plugins`): **`/brain:setup`**.

> Os comandos de plugin levam o nome do plugin na frente: é **`/brain:setup`**. Digite `/brain:` para ver todos.

## Onboarding em 5 minutos (`/brain:setup`)
1. **Onde fica o cofre** (padrão `~/Brain`) e **quais áreas da vida** (pessoal, trabalho, projetos, estudos ou as suas).
2. **Quais projetos ligar:** ele lista as pastas onde você mais usou o Claude Code e propõe a área de cada uma; você só marca.
3. **Graphify (recomendado):** seguir ou não com o mapa do código. Depois, opcionais: [Obsidian](https://obsidian.md)
   para ver as notas e git no cofre.
4. **Prova:** mostra o contexto que a próxima conversa vai receber.

## Graphify: recomendado para economizar tokens
O [Graphify](https://pypi.org/project/graphifyy/) (grátis, local, sem LLM) gera um **mapa do código** de cada projeto.
Com ele, o Claude consulta o mapa antes de abrir arquivos, e a pergunta típica custa **dezenas de vezes menos tokens**
em projeto grande. Em dois repositórios reais, o `graphify benchmark` mediu ~15x e ~270x menos tokens por pergunta.
O Brain funciona sem ele, mas com ele você ganha:
- **Mapa do código** no contexto de cada conversa e no cofre (`Mapa/`), refeito sozinho a cada commit;
- **Grafo global** (`~/.graphify/global-graph.json`): todos os repos ligados num grafo só, para perguntas que cruzam projetos;
- **`/brain:medir`**: mostra quanto você está economizando (benchmark e teste A/B).

O `/brain:setup` pergunta se você quer seguir com ele e instala (`pipx install graphifyy`). Dá para ligar depois com `/brain:conectar`.

## Como funciona
O plugin traz hooks próprios, então você não edita `settings.json` nem `CLAUDE.md`:
- **Início de cada conversa:** se a pasta é de um projeto, o Claude recebe a área dele, o `Status.md`, as 3 decisões mais
  recentes e o mapa do código, e abre a primeira resposta com "onde paramos · pendente · próximo passo". Fora de projeto,
  recebe só o índice das áreas (barato).
- **Fim de cada resposta:** o diário da sessão (pedidos, ações, arquivos, pesquisas, commits) é atualizado em
  `inbox/sessoes/`. Sem LLM, só extração. Nada vira nota sem o `/brain:revisar`.
- **Carregamento em camadas:** só o índice sempre; a área inteira ao abrir um projeto; nota completa sob demanda.
  O `resumo` de uma linha de cada nota é o que entra no contexto.

| Comando | Quando |
|---|---|
| `/brain:setup` | primeira vez, ou para conectar mais pastas |
| `/brain:fechar` | fim do trabalho: atualiza o Status (feito, pendente, próximo passo, erros) |
| `/brain:decisao` | escolheu um rumo: contexto, opções, motivo, como desfazer |
| `/brain:lembrar <fato>` | fato, preferência ou link que deve valer nas próximas conversas |
| `/brain:revisar` | decide o que do diário vira Status, Decisão ou nota |
| `/brain:conectar` | liga uma pasta nova a um projeto (e, se quiser, o mapa do código) |
| `/brain:consultar <assunto>` | o que o Brain sabe sobre algo |
| `/brain:pesquisar <tarefa>` | antes de algo novo: reaproveita pesquisas, busca a melhor forma e registra |
| `/brain:medir` | (com Graphify) quanto o mapa do código economiza de tokens |

## Privacidade
- Tudo fica no seu computador: o cofre onde você escolher e a configuração em `~/.brain/config.json`.
- O `/brain:setup` lê de `~/.claude/projects` só o caminho das pastas onde você usou o Claude Code, para sugerir projetos.
- As notas nunca guardam senha, chave, token ou valor financeiro. Se for versionar o cofre, use repositório **privado**.

## Desinstalar
`/plugin uninstall brain@brain`. O cofre é seu e continua onde está; apague `~/.brain/` se quiser.

Licença MIT.
