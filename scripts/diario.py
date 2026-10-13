#!/usr/bin/env python3
"""Diário de sessão do Brain: lê a transcrição de uma sessão do Claude Code e mantém um resumo em <cofre>/inbox/sessoes/.

Chamado pelos hooks Stop (a cada resposta) e SessionEnd, em segundo plano, com o JSON do hook no stdin
(session_id, transcript_path, cwd). Sem LLM: só extrai o que aconteceu. A decisão do que vira nota do Brain é do
`/brain:revisar`.

  python3 diario.py < hook.json                 # uso pelos hooks
  python3 diario.py --transcript X.jsonl --cwd DIR
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brain  # noqa: E402

SAIDA = brain.ROOT / "inbox" / "sessoes" if brain.ROOT else None

RUIDO = ("<", "[Image", "Caveat:", "[Request interrupted")


def limpa(t, n=280):
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def ler(transcript):
    pedidos, feitos, arquivos, buscas, paginas, skills = [], [], {}, [], [], []
    titulo, inicio, fim, sessao = None, None, None, None
    for linha in open(transcript, encoding="utf-8", errors="ignore"):
        try:
            d = json.loads(linha)
        except ValueError:
            continue
        sessao = sessao or d.get("sessionId")
        ts = d.get("timestamp")
        if ts:
            inicio = inicio or ts
            fim = ts
        if d.get("type") == "ai-title":
            titulo = d.get("aiTitle") or titulo
        msg = d.get("message") or {}
        conteudo = msg.get("content")
        if d.get("type") == "user" and isinstance(conteudo, str) and (d.get("origin") or {}).get("kind", "human") == "human":
            t = conteudo.strip()
            if t and not t.startswith(RUIDO) and (not pedidos or pedidos[-1] != limpa(t)):
                pedidos.append(limpa(t))
        if d.get("type") == "assistant" and isinstance(conteudo, list):
            for it in conteudo:
                if it.get("type") != "tool_use":
                    continue
                nome, inp = it.get("name"), it.get("input") or {}
                if nome == "Bash" and inp.get("description"):
                    if inp["description"] not in feitos:
                        feitos.append(inp["description"])
                elif nome in ("Write", "Edit", "NotebookEdit") and inp.get("file_path"):
                    arquivos.setdefault(inp["file_path"], set()).add("criado" if nome == "Write" else "editado")
                elif nome == "WebSearch" and inp.get("query"):
                    buscas.append(limpa(inp["query"], 140))
                elif nome == "WebFetch" and inp.get("url"):
                    paginas.append(inp["url"])
                elif nome == "Skill" and inp.get("skill"):
                    if inp["skill"] not in skills:
                        skills.append(inp["skill"])
    return {"sessao": sessao, "titulo": titulo, "inicio": inicio, "fim": fim, "pedidos": pedidos, "feitos": feitos,
            "arquivos": arquivos, "buscas": buscas, "paginas": paginas, "skills": skills}


def commits(cwd, desde):
    if not desde:
        return []
    try:
        r = subprocess.run(["git", "-C", cwd, "log", f"--since={desde}", "--format=%h %s"], capture_output=True, text=True, timeout=10)
        return [x for x in r.stdout.splitlines() if x.strip()]
    except Exception:
        return []


def rel(p, cwd):
    try:
        return str(Path(p).resolve().relative_to(Path(cwd).resolve()))
    except ValueError:
        return p.replace(str(Path.home()), "~")


def gerar(transcript, cwd):
    s = ler(transcript)
    if not s["sessao"] or (not s["pedidos"] and not s["arquivos"]):
        return None
    notes, _ = brain.load()
    proj = brain.match_note(notes, cwd)
    pid = proj["id"] if proj else Path(cwd).name
    modulo = proj["modulo"] if proj else None
    dia = (s["inicio"] or datetime.now().isoformat())[:10]
    destino = SAIDA / f"{dia}-{re.sub(r'[^a-z0-9-]+', '-', pid.lower())}-{s['sessao'][:8]}.md"
    status = "pendente"
    if destino.exists():  # preserva a revisão já feita
        m = re.search(r"^status: (\S+)", destino.read_text(encoding="utf-8"), re.M)
        status = m.group(1) if m else status
    def hora(t):
        try:
            return datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone().strftime("%H:%M")
        except (AttributeError, ValueError):
            return ""
    out = ["---", "tipo: sessao", f"projeto: {pid}", f"modulo: {modulo or 'sem módulo'}", f"sessao: {s['sessao']}",
           f"pasta: {cwd}", f"data: {dia}", f"inicio: {hora(s['inicio'])}", f"fim: {hora(s['fim'])}",
           f"status: {status}", "---",
           f"# Sessão · {pid} · {dia}" + (f" · {s['titulo']}" if s["titulo"] else ""), "",
           f"Projeto: {'[[' + pid + ']]' if proj else pid + ' (pasta sem projeto no Brain)'} · status da revisão: **{status}**", ""]
    out += ["## O que eu pedi"] + [f"{i}. {p}" for i, p in enumerate(s["pedidos"], 1)] + [""]
    if s["feitos"]:
        out += ["## O que foi feito"] + [f"- {f}" for f in s["feitos"][:60]] + ([f"- … e mais {len(s['feitos']) - 60}"] if len(s["feitos"]) > 60 else []) + [""]
    if s["arquivos"]:
        out += ["## Arquivos criados ou alterados"] + [f"- `{rel(p, cwd)}` ({', '.join(sorted(k))})" for p, k in sorted(s["arquivos"].items())] + [""]
    if s["buscas"] or s["paginas"]:
        out += ["## Pesquisas"] + [f"- busca: {b}" for b in s["buscas"]] + [f"- página: {u}" for u in s["paginas"]] + [""]
    if s["skills"]:
        out += ["## Skills usadas", "- " + ", ".join(s["skills"]), ""]
    cs = commits(cwd, s["inicio"])
    if cs:
        out += ["## Commits nesta sessão"] + [f"- {c}" for c in cs] + [""]
    out += ["## Revisão (preenchida pelo /brain:revisar)", "- [ ] Vira nota ou atualização no Brain?", "- [ ] Decisão para registrar?",
            "- [ ] Atualizar Status do projeto?", ""]
    SAIDA.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(out), encoding="utf-8")
    return destino


def main():
    if "--transcript" in sys.argv:
        t = sys.argv[sys.argv.index("--transcript") + 1]
        cwd = sys.argv[sys.argv.index("--cwd") + 1] if "--cwd" in sys.argv else os.getcwd()
    else:
        try:
            ev = json.load(sys.stdin)
        except ValueError:
            return 0
        t, cwd = ev.get("transcript_path"), ev.get("cwd") or os.getcwd()
    if not SAIDA or not t or not Path(t).exists():
        return 0
    if "/scratchpad" in cwd:
        return 0  # pasta temporária de subagente: não vira diário
    dest = gerar(t, cwd)
    if dest and "--verbose" in sys.argv:
        print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
