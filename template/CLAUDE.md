# Brain (cofre)

Cofre de notas em markdown, aberto no Obsidian (opcional). O plugin Brain do Claude Code lê este cofre em toda conversa.

## Estrutura
- `Inicio.md`: página inicial. `INDEX.md`: mapa gerado (entra no contexto), não editar à mão.
- `Projetos.base`, `Decisoes.base`: painéis do Obsidian Bases.
- `modulos/<área>/_index.md`: raiz da área (`tipo: raiz`, opcional `usa: [...]` se depender de outra área).
- `modulos/<área>/<projeto>/`: `<projeto>.md` (`tipo: projeto`, `paths:`), `Status.md` (`id: status-<projeto>`),
  `Decisoes/AAAA-MM-DD <título>.md` (`tipo: decisao`), `Decisoes.base`, `Mapa/` (gerado pelo Graphify, se ligado).
- `modulos/<área>/*.md`: notas soltas da área (`tipo: sub`), pesquisas (`tipo: pesquisa`).
- `referencias/`: fontes externas resumidas. `inbox/`: material cru. `inbox/sessoes/`: diário automático (fora do git).

## Regras de escrita
- Frontmatter: `id` único (ou nome de arquivo único), `tipo`, `resumo` de uma linha (é o que vai para o contexto), `tags`.
- Toda nota liga para a raiz da área ou para o projeto; a raiz lista as notas dela.
- Uma ideia por nota. O Brain guarda fatos estáveis, status, decisões e ponteiros; conteúdo grande fica no projeto.
- Nada de senha, chave, token, valor financeiro ou dado pessoal sensível. Datas AAAA-MM-DD.
- Depois de editar: `brain.py lint` e `brain.py index` (o plugin sabe o caminho).
