#!/usr/bin/env python3
"""
LLM Atlas Pro — aggiornamento automatico della sezione "Novità dal mondo dell'IA".

Usa l'API di Claude (con web search) per recuperare le ultime novità dell'IA,
le riassume in italiano e le inserisce in index.html tra i marcatori
<!-- NEWS:START --> e <!-- NEWS:END -->.

⚠️ SICUREZZA: la tua API key NON deve MAI finire dentro index.html (che è pubblico
su GitHub Pages). Questo script gira in LOCALE sul tuo PC e legge la key da un file
.env che NON viene caricato su GitHub (vedi .gitignore). La key resta sul tuo computer.

Uso:
    1. pip install -r scripts/requirements.txt
    2. copia .env.example in .env e incolla la tua key (da console.anthropic.com)
    3. python scripts/update_news.py            # aggiorna la sezione
    4. python scripts/update_news.py --push     # aggiorna e fa git push
"""

import os
import re
import sys
import subprocess
from datetime import date
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("Manca la libreria 'anthropic'. Esegui: pip install -r scripts/requirements.txt")

# Carica la API key dal file .env (mai committato)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass  # se manca python-dotenv, prova comunque dall'ambiente

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
MODEL = "claude-opus-4-8"

PROMPT = (
    "Sei un divulgatore esperto di IA, nello stile dei migliori post LinkedIn: "
    "spieghi, non elenchi. Cerca sul web le novità più importanti del mondo "
    "dell'intelligenza artificiale degli ultimi giorni (modelli, paper, agenti, "
    "prodotti, regolamentazione). Scrivi IN ITALIANO per una studentessa di 18 "
    "anni che vuole diventare elite nell'IA. "
    "Produci ESATTAMENTE 5 notizie. Per OGNUNA usa questa struttura: "
    "titolo in grassetto, poi UNA frase su cosa è successo, UNA su perché conta "
    "davvero, e UNA su cosa significa per chi studia IA (inizia con '→ Per te:'). "
    "Sii concreto, niente hype. "
    "Restituisci SOLO frammento HTML in questo formato, senza altro testo:\n"
    "<ul style=\"margin:0; padding-left:1.2rem;\">\n"
    "<li style=\"margin-bottom:14px;\"><b>Titolo</b> — cosa è successo. "
    "Perché conta. <i>→ Per te: cosa significa.</i></li>\n"
    "... (5 voci)\n"
    "</ul>"
)


def fetch_news() -> str:
    """Chiede a Claude (con web search) le ultime novità e ritorna un frammento HTML."""
    client = anthropic.Anthropic()  # legge ANTHROPIC_API_KEY dall'ambiente / .env

    messages = [{"role": "user", "content": PROMPT}]
    tools = [{"type": "web_search_20260209", "name": "web_search"}]

    # Loop per gestire pause_turn (la web search è un tool server-side)
    for _ in range(6):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            tools=tools,
            messages=messages,
        )
        if resp.stop_reason == "pause_turn":
            messages = [
                {"role": "user", "content": PROMPT},
                {"role": "assistant", "content": resp.content},
            ]
            continue
        break

    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    # Tieni solo da <ul> a </ul> se il modello ha aggiunto preamboli
    m = re.search(r"<ul[\s\S]*</ul>", text)
    return m.group(0) if m else text


def update_index(news_html: str) -> None:
    html = INDEX.read_text(encoding="utf-8")
    today = date.today().strftime("%d/%m/%Y")
    block = (
        "<!-- NEWS:START -->\n"
        f'    <div style="font-size:0.7rem; letter-spacing:1px; text-transform:uppercase; '
        f'color:var(--text2); margin-bottom:10px;">Aggiornato il {today}</div>\n'
        '    <div style="font-size:0.88rem; color:var(--text2); line-height:1.7;">\n'
        f"    {news_html}\n"
        "    </div>\n"
        "    <!-- NEWS:END -->"
    )
    new_html, n = re.subn(
        r"<!-- NEWS:START -->[\s\S]*?<!-- NEWS:END -->",
        block,
        html,
    )
    if n == 0:
        sys.exit("Marcatori <!-- NEWS:START --> / <!-- NEWS:END --> non trovati in index.html")
    INDEX.write_text(new_html, encoding="utf-8")
    print(f"index.html aggiornato (sezione Novità, {today}).")


def git_push() -> None:
    subprocess.run(["git", "-C", str(ROOT), "add", "index.html"], check=True)
    subprocess.run(
        ["git", "-C", str(ROOT), "commit", "-m", f"Aggiorna Novità IA ({date.today().isoformat()})"],
        check=True,
    )
    subprocess.run(["git", "-C", str(ROOT), "push"], check=True)
    print("Modifiche pushate su GitHub.")


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit(
            "ANTHROPIC_API_KEY non trovata. Copia .env.example in .env e incolla la tua key.\n"
            "La trovi su https://console.anthropic.com"
        )
    print("Recupero le ultime novità dall'IA (può richiedere ~30s)...")
    news = fetch_news()
    update_index(news)
    if "--push" in sys.argv:
        git_push()
    else:
        print("Fatto. Per pubblicare: python scripts/update_news.py --push")


if __name__ == "__main__":
    main()
