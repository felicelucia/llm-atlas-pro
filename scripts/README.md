# 📰 Self-update della sezione "Novità"

Questo script aggiorna automaticamente la sezione **Novità dal mondo dell'IA** del sito,
usando l'API di Claude per cercare sul web le ultime novità e riassumerle in italiano.

## 🔒 Sicurezza prima di tutto

La tua **API key non finisce MAI dentro il sito**. Il sito (`index.html`) è pubblico su
GitHub Pages: se la key fosse lì, chiunque potrebbe vederla e spendere i tuoi soldi.

Questo script gira **in locale sul tuo PC** e legge la key da un file `.env` che
**non viene caricato su GitHub** (è escluso dal `.gitignore`). La key resta sul tuo computer.

## Come si usa

### 1. Installa le dipendenze (una volta sola)
```powershell
pip install -r scripts/requirements.txt
```

### 2. Crea il file con la tua key (una volta sola)
- Copia `.env.example` in un nuovo file chiamato `.env`
- Apri `.env` e incolla la tua API key (la trovi su https://console.anthropic.com)

### 3. Aggiorna le novità
```powershell
# Solo aggiorna il file locale (per controllarlo prima)
python scripts/update_news.py

# Aggiorna E pubblica online (git push automatico)
python scripts/update_news.py --push
```

## Quanto costa

Ogni aggiornamento fa una manciata di chiamate API con web search — pochi centesimi.
Puoi lanciarlo quando vuoi (es. una volta a settimana).

## Automatizzarlo (opzionale, avanzato)

Su Windows puoi usare l'**Utilità di pianificazione** per lanciare
`python scripts/update_news.py --push` ogni settimana automaticamente.
