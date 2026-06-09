# 🧭 LLM Atlas Pro

> Il percorso per diventare elite nell'IA — **costruendo cose reali e divertendoti.**
> Non una lista di ore che spaventa, ma un percorso a missioni, aggiornato a giugno 2026.

### 🌐 [Apri il sito → felicelucia.github.io/llm-atlas-pro](https://felicelucia.github.io/llm-atlas-pro/)

---

## Cosa contiene

Un'unica pagina interattiva (`index.html`, funziona offline) che raccoglie:

- **13 blocchi di percorso** — da matematica e Python fino a reasoning models, quantum AI, EU AI Act e sicurezza degli agenti
- **Labs interattivi** — Python in-browser (Pyodide), visualizzazioni animate, quiz
- **Progetti & strategia** — Missione Giorno 1, il progetto che cresce con te, BioBridge (salute), QuantLab (finanza), Olimpiadi di matematica, il capstone "Il Salto"
- **Approfondimenti** — costruisci un Mamba, anatomia dei progetti virali su GitHub, il playbook di Jensen Huang
- **Snack di matematica** e la mentalità che ti rende assumibile dai lab
- Sistema a livelli: 🟢 Base · 🔵 Approfondimento · 🟣 Elite

## Struttura del repo

```
index.html                      il sito (tutto qui dentro)
guides/costruisci-un-mamba.md   guida passo-passo per costruire un Mamba
scripts/update_news.py          aggiorna la sezione "Novità" via API Claude (in locale)
scripts/README.md               come usare lo script in sicurezza
```

## Aggiornare le "Novità" automaticamente

Lo script `scripts/update_news.py` usa l'API di Claude per recuperare le ultime novità
dell'IA e aggiornare la sezione Novità. La tua API key resta **in locale** (file `.env`,
mai caricato su GitHub). Vedi [`scripts/README.md`](scripts/README.md).

## Modificare il sito

Apri `index.html`, modifica, poi:

```powershell
git add .
git commit -m "descrizione modifica"
git push
```

Il sito si aggiorna da solo in pochi secondi.

---

*Costruito come progetto educativo. Buon viaggio verso l'elite dell'IA. 🚀*
