# Guia do Brain em 1 página

O Brain dá memória ao Claude Code. Ele guarda cada projeto numa pasta de notas no seu computador, e toda conversa nova
já abre com onde você parou, o que falta e o próximo passo.

## 1. Instalar (2 comandos, uns 5 minutos)
Precisa do [Claude Code](https://claude.com/claude-code) (plano pago ou chave de API) e do Python 3.9+. Dentro do Claude Code:
```
/plugin install brain --marketplace JoaoVitorOCS/brain
/brain:setup
```
O setup faz 3 perguntas: onde guardar o cofre (padrão `~/Brain`), quais áreas da sua vida (pessoal, trabalho,
projetos…) e quais pastas ligar. Ele lista as pastas onde você mais usou o Claude Code, então você só marca.

**O comando não aparece?** Rode `/reload-plugins` ou abra uma conversa nova. Comando de plugin leva o nome na frente:
é `/brain:setup`, com dois-pontos. E `/plugin marketplace add` sozinho não instala nada; use o comando acima.

## 2. O dia a dia
| Quando | O que fazer |
|---|---|
| Abriu uma conversa num projeto | nada: a 1ª resposta já traz onde você parou, o pendente e o próximo passo |
| Terminou o trabalho | `/brain:fechar` atualiza o Status do projeto. É ele que faz a próxima conversa saber onde parar |
| Escolheu um rumo (ferramenta, arquitetura, preço) | `/brain:decisao` guarda o contexto, as opções, o motivo e como desfazer |
| Algo que deve valer sempre ("prefiro respostas curtas", "sou designer") | `/brain:lembrar <fato>` |
| Uma vez por semana | `/brain:revisar`: cada sessão vira um diário em `inbox/sessoes/`, e você decide o que vira nota |
| Pasta nova que vai durar | `/brain:conectar` |
| "O que eu decidi sobre X?" | `/brain:consultar <assunto>` |
| Antes de começar algo novo | `/brain:pesquisar <tarefa>` busca a melhor forma grátis e registra |

Se você só criar um hábito, crie o do `/brain:fechar`.

## 3. Medir a sua economia de tokens
A economia grande vem do **Graphify** (grátis, local, sem IA): ele gera um mapa do código de cada projeto, e o Claude
consulta o mapa em vez de abrir arquivo por arquivo.
1. Instale: `pipx install graphifyy` (ou `pip install graphifyy`).
2. No Claude Code, dentro da pasta do projeto: `/brain:conectar` e aceite o mapa do código.
3. Rode `/brain:medir`. Ele mostra, por projeto, quantos tokens custaria ler tudo e quanto custa uma pergunta pelo mapa.

O número é um teto, porque compara com ler o projeto inteiro. Em dois repositórios reais deu ~15x e ~270x menos tokens
por pergunta; num projeto pequeno a economia é menor. Para medir no uso de verdade, o `/brain:medir` explica um teste A/B
com duas conversas e o `/context`.

## 4. Onde ficam as coisas
- Notas: o cofre que você escolheu (abre no [Obsidian](https://obsidian.md), se quiser ver os links e painéis).
- Configuração: `~/.brain/config.json`.
- Nada sai do seu computador. Não guarde senha, chave ou valor financeiro nas notas. Se versionar o cofre no GitHub,
  use repositório privado.

Dúvida ou problema: abra uma issue em https://github.com/JoaoVitorOCS/brain/issues.
