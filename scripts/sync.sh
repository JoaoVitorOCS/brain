#!/bin/sh
# Sincroniza o cofre do Brain com o repositório git dele (ex.: o mesmo cofre no Windows e no Linux).
#   sync.sh pull   puxa o remoto (hook SessionStart, antes do contexto); silencioso se der certo
#   sync.sh push   commit de tudo + pull --rebase + push (fim do /brain:fechar)
# Não faz nada se o cofre não for repositório git com remoto `origin`. Nunca pede senha (GIT_TERMINAL_PROMPT=0).
DIR_SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
COFRE="$(python3 "$DIR_SCRIPTS/brain.py" onde 2>/dev/null)"
[ -d "$COFRE/.git" ] || exit 0
cd "$COFRE" || exit 0
git remote get-url origin >/dev/null 2>&1 || exit 0
export GIT_TERMINAL_PROMPT=0
T=""; command -v timeout >/dev/null 2>&1 && T="timeout 8"

puxar() {
  if ! $T git pull --rebase --autostash -q >/dev/null 2>&1; then
    if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
      git rebase --abort >/dev/null 2>&1
      echo "> Brain: conflito ao sincronizar o cofre ($COFRE). Nada foi perdido; resolva com \`git -C \"$COFRE\" pull --rebase\`."
    else
      echo "> Brain: não consegui puxar o cofre do remoto (sem rede?). Usando a cópia local."
    fi
    return 1
  fi
}

case "$1" in
  pull)
    puxar
    ;;
  push)
    git add -A
    if ! git diff --cached --quiet; then
      git commit -qm "brain: $(hostname 2>/dev/null || echo maquina) $(date +%Y-%m-%d\ %H:%M)" || exit 1
    fi
    puxar || exit 1
    if [ -n "$(git log '@{u}..' --oneline 2>/dev/null)" ]; then
      $T git push -q >/dev/null 2>&1 && echo "cofre enviado ao remoto" || { echo "falha no push do cofre (rode \`git -C \"$COFRE\" push\`)"; exit 1; }
    else
      echo "cofre já sincronizado"
    fi
    ;;
  *)
    echo "uso: sync.sh pull|push"; exit 1
    ;;
esac
exit 0
