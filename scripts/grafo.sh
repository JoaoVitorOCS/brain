#!/bin/sh
# Graphify (opcional) para o Brain. Sem LLM e sem custo de token: grafo estrutural do código (AST + markdown).
#   grafo.sh ligar <pasta> [<id-do-projeto>]   liga o Graphify num repo (fora do git, hooks de commit, grafo global, Mapa no cofre)
#   grafo.sh atualizar <pasta>                 refaz o grafo, o grafo global e o Mapa se a pasta já tem grafo (hook SessionStart)
# Grafo global (~/.graphify/global-graph.json): todos os repos ligados num grafo só, para perguntas entre projetos.
DIR_SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
GRAPHIFY="$(command -v graphify 2>/dev/null || ls "$HOME/.local/bin/graphify" 2>/dev/null)"
ACAO="$1"; DIR="${2:-$PWD}"; ID="${3:-}"
[ -n "$GRAPHIFY" ] || { [ "$ACAO" = ligar ] && echo "graphify não instalado (pipx install graphifyy ou pip install graphifyy)"; exit 0; }
cd "$DIR" 2>/dev/null || exit 0

if [ "$ACAO" = atualizar ]; then
  [ -f graphify-out/graph.json ] || exit 0
  LOCK="graphify-out/.atualizando"
  mkdir "$LOCK" 2>/dev/null || exit 0
  trap 'rmdir "$LOCK" 2>/dev/null' EXIT
  PYTHONHASHSEED=0 "$GRAPHIFY" update . >/dev/null 2>&1
  "$GRAPHIFY" global add graphify-out/graph.json --as "$(basename "$DIR")" >/dev/null 2>&1
  python3 "$DIR_SCRIPTS/brain.py" mapa --cwd "$DIR" >/dev/null 2>&1
  exit 0
fi

# ligar: graphify-out fica fora do git só nesta máquina (.git/info/exclude não é versionado)
if GITDIR="$(git rev-parse --git-dir 2>/dev/null)"; then
  case "$GITDIR" in /*) ;; *) GITDIR="$DIR/$GITDIR" ;; esac
  mkdir -p "$GITDIR/info"
  grep -qx 'graphify-out/' "$GITDIR/info/exclude" 2>/dev/null || echo 'graphify-out/' >> "$GITDIR/info/exclude"
fi
PYTHONHASHSEED=0 "$GRAPHIFY" update . 2>&1 | grep -E "Rebuilt" || true
if [ -n "${GITDIR:-}" ]; then
  had_attr=0; [ -e .gitattributes ] && had_attr=1
  "$GRAPHIFY" hook install >/dev/null 2>&1 || true
  # o merge driver só serve quando graph.json é versionado; aqui não é
  if [ "$had_attr" = 0 ] && [ -e .gitattributes ] && ! grep -qv 'merge=graphify' .gitattributes; then
    rm .gitattributes
  elif [ -e .gitattributes ]; then
    sed -i.bak '/merge=graphify/d' .gitattributes && rm -f .gitattributes.bak
  fi
  git config --local --remove-section merge.graphify 2>/dev/null || true
fi
"$GRAPHIFY" global add graphify-out/graph.json --as "$(basename "$DIR")" 2>&1 | tail -1
[ -n "$ID" ] && python3 "$DIR_SCRIPTS/brain.py" mapa "$ID"
exit 0
