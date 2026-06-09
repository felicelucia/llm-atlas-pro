# 🐍 Costruisci un Mamba — guida passo-passo

> Una guida pratica per costruire da zero un piccolo modello **Mamba** (state space model),
> l'alternativa elegante al Transformer. Pensata per chi sa già un po' di Python e ha
> capito le basi delle reti neurali (blocco 02 del percorso). Alla fine avrai un modello
> che genera testo **e** un teardown da mettere nel portfolio.

---

## Perché Mamba (in 30 secondi)

Un **Transformer**, per generare la parola numero *n*, riguarda *tutte* le *n-1* parole
precedenti tramite l'attention. È potente ma costa **O(n²)**: più lunga è la sequenza,
più esplode il calcolo.

**Mamba** fa una cosa diversa: mantiene uno **stato compresso** che aggiorna passo dopo
passo, come una memoria che scorre. Il colpo di genio è renderlo **selettivo**: il modello
decide *cosa ricordare e cosa dimenticare* in base all'input. Risultato: scala **lineare**
nella lunghezza della sequenza e gestisce contesti lunghissimi.

È un'idea che viene dalla **teoria dei sistemi di controllo** (state space models), portata
nel deep learning. Costruirne uno ti fa capire le architetture in profondità — una cosa
rara, soprattutto se parti da giovane.

---

## Cosa ti serve

- Python 3.10+, con `numpy` e `torch` (PyTorch)
- Un po' di pazienza e curiosità
- Hardware: gira anche su un PC normale (modello piccolo). Per andare più veloce,
  una GPU gratuita su [Google Colab](https://colab.research.google.com) è perfetta.

```powershell
pip install torch numpy
```

---

## Livello 1 — 🟢 Capisci l'intuizione (prima di toccare il codice)

Non saltare questo passo. Leggi/guarda in quest'ordine:

1. **[A Visual Guide to Mamba](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mamba-and-state)** — Maarten Grootendorst. La spiegazione visiva più chiara: capisci *perché* gli state space model funzionano e cos'è la "selettività".
2. Tieni a portata di mano il paper originale **[Mamba (Gu & Dao, 2023)](https://arxiv.org/abs/2312.00752)** — non leggerlo tutto ora, lo userai come riferimento.

**Obiettivo:** sapere spiegare a voce, senza codice, cosa fa lo stato selettivo. Se ci
riesci, sei pronto.

---

## Livello 2 — 🟢 Leggi un'implementazione minimale

Studia **[mamba-minimal](https://github.com/johnma2006/mamba-minimal)** di johnma2006:
è Mamba in **un solo file PyTorch leggibile**, senza i kernel CUDA ottimizzati. Perfetto
per imparare.

Apri `model.py` e identifica i pezzi chiave:
- `MambaBlock` — il blocco che fa il lavoro
- la **selective scan** — il cuore: dove lo stato viene aggiornato passo per passo
- le proiezioni di input/output

Disegna su carta come fluiscono i dati: `input → proiezione → scan selettivo → output`.

---

## Livello 3 — 🔵 Costruisci il TUO mini-Mamba

Adesso scrivi tu il codice. Ecco lo scheletro di un singolo blocco Mamba semplificato —
completalo seguendo mamba-minimal e il tuo disegno:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MiniMambaBlock(nn.Module):
    def __init__(self, d_model, d_state=16, expand=2):
        super().__init__()
        self.d_inner = expand * d_model
        # proietta l'input nello spazio interno (x e gate z)
        self.in_proj = nn.Linear(d_model, self.d_inner * 2)
        # convoluzione causale 1D (mescola un po' nel tempo)
        self.conv1d = nn.Conv1d(self.d_inner, self.d_inner, kernel_size=3,
                                groups=self.d_inner, padding=2)
        # parametri dello state space (dipendono dall'input → "selettivi")
        self.x_proj = nn.Linear(self.d_inner, d_state * 2 + 1)
        self.dt_proj = nn.Linear(1, self.d_inner)
        # A: matrice di stato (log per stabilità); D: skip connection
        self.A_log = nn.Parameter(torch.log(torch.arange(1, d_state + 1).float()
                                             .repeat(self.d_inner, 1)))
        self.D = nn.Parameter(torch.ones(self.d_inner))
        self.out_proj = nn.Linear(self.d_inner, d_model)

    def forward(self, x):
        # x: (batch, lunghezza, d_model)
        b, l, _ = x.shape
        xz = self.in_proj(x)                      # (b, l, 2*d_inner)
        x_in, z = xz.chunk(2, dim=-1)
        # conv causale
        x_in = x_in.transpose(1, 2)
        x_in = self.conv1d(x_in)[:, :, :l].transpose(1, 2)
        x_in = F.silu(x_in)
        # --- QUI implementa la SELECTIVE SCAN ---
        # 1. ricava dt, B, C da self.x_proj(x_in)
        # 2. discretizza A con dt
        # 3. scorri nel tempo aggiornando lo stato h:  h = dA*h + dB*x ; y = C*h
        # (segui mamba-minimal: funzione selective_scan)
        y = self.selective_scan(x_in)             # <-- da scrivere
        y = y * F.silu(z)                         # gate
        return self.out_proj(y)

    def selective_scan(self, x):
        # TODO: implementa lo scan selettivo seguendo mamba-minimal
        raise NotImplementedError
```

**Sfida:** completa `selective_scan`. È il pezzo che conta — quando funziona, hai capito
Mamba davvero.

### Allenalo su un piccolo testo
Riusa l'approccio di **makemore / nanoGPT** (blocco 02): prendi un file di testo (es. le
poesie di Dante, o i tuoi messaggi), tokenizza a livello di carattere, impila qualche
`MiniMambaBlock`, e allena a predire il carattere successivo. Poi fai generare testo e
guarda cosa "scrive".

### Confrontalo con un Transformer
Allena anche un mini-Transformer (nanoGPT) sullo stesso dataset. Confronta: qualità del
testo, velocità, memoria usata al crescere della lunghezza. **Questo confronto è oro per
il tuo teardown.**

---

## Livello 4 — 🟣 Scrivi il teardown (il vero salto)

Questo è il passo che ti fa notare. Scrivi un post / README che spiega Mamba **come lo
spiegheresti a un'amica**, con i tuoi disegni e i tuoi risultati:

- Cos'è uno state space model, con un'immagine tua
- Cos'è la selettività e perché cambia tutto
- Il tuo codice, commentato
- Il confronto Mamba vs Transformer con i tuoi numeri/grafici
- Cosa hai imparato e dove ti sei bloccata (l'onestà piace)

Pubblicalo su GitHub + un blog (anche un semplice post). **Spiegare chiaro è metà del
valore** — è ciò che professori e lab notano.

---

## Per andare oltre (🟣 opzionale)

- **[The Annotated S4](https://srush.github.io/annotated-s4/)** — Sasha Rush: il precursore di Mamba (S4) spiegato col codice. Per capire la matematica a fondo.
- **[state-spaces/mamba](https://github.com/state-spaces/mamba)** — il repo ufficiale con i kernel CUDA ottimizzati. Guarda come si fa "sul serio" a livello hardware (si collega al blocco CUDA del percorso).

---

## Checklist

- [ ] So spiegare a voce cos'è lo stato selettivo
- [ ] Ho letto e capito `mamba-minimal`
- [ ] Ho scritto il mio `MiniMambaBlock` con la selective scan funzionante
- [ ] L'ho allenato su un testo e genera qualcosa di sensato
- [ ] L'ho confrontato con un mini-Transformer
- [ ] Ho pubblicato un teardown con codice + risultati

Quando li spunti tutti, hai un capstone vero in mano. 🚀
