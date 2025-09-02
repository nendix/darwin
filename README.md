# Darwin - Simulatore di Evoluzione con Algoritmi Genetici

![Darwin Logo](https://img.shields.io/badge/Darwin-Evolution%20Simulator-green)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-red)

## 🧬 Panoramica

Darwin è un simulatore di evoluzione 2D che utilizza algoritmi genetici per simulare l'evoluzione di due specie: predatori e prede. Il progetto dimostra i principi dell'evoluzione naturale attraverso selezione, riproduzione, mutazione e adattamento ambientale.

## ✨ Caratteristiche Principali

### 🎯 Simulazione Genetica
- **Due specie distinte**: Predatori (cacciatori) e Prede (sopravviventi)
- **Genomi diversificati**: Ogni specie ha tratti genetici specifici
- **Evoluzione in tempo reale**: Osserva l'evoluzione mentre accade
- **Algoritmi genetici**: Crossover, mutazione e selezione naturale

### 🎮 Interfaccia Utente
- **Menu principale**: Configurazione parametri di simulazione
- **Simulazione interattiva**: Visualizzazione in tempo reale
- **Schermata statistiche**: Analisi dettagliate dei risultati
- **Controlli intuitivi**: Navigazione con tastiera e mouse

### 📊 Sistema di Analisi
- **Statistiche avanzate**: Tracking delle popolazioni nel tempo
- **Grafici evolutivi**: Visualizzazione dell'andamento genetico
- **Report completi**: Esportazione in formato HTML
- **Analisi delle tendenze**: Identificazione dei pattern evolutivi

## 🧮 Genomi delle Specie

### Predatori
- **Velocità**: Velocità di movimento (1-100)
- **Visione**: Raggio visivo a cono (1-100)
- **Stamina**: Capacità energetica massima (1-100)
- **Forza Attacco**: Potenza degli attacchi (1-100)

### Prede
- **Velocità**: Velocità di movimento (1-100)
- **Visione**: Raggio visivo a 360° (1-100)
- **Stamina**: Capacità energetica massima (1-100)
- **Resistenza**: Resistenza agli attacchi (1-100)

## 🎮 Meccaniche di Gioco

### Comportamenti
- **Predatori**: Cacciano le prede, si riproducono quando raggiungono il punteggio
- **Prede**: Evitano i predatori, mangiano cibo, si riproducono
- **Collisioni**: Predatore vs Preda = attacco, Preda vs Cibo = nutrimento

### Sistema Energetico
- **Consumo**: L'energia diminuisce con movimento e tempo
- **Rigenerazione**: Mangiare cibo ripristina l'energia
- **Morte**: Energia = 0 o essere mangiati

### Riproduzione
- **Soglia**: Punteggio di 100 per potersi riprodurre
- **Crossover**: Combinazione genetica tra due genitori
- **Mutazione**: Variazioni casuali nei geni della prole

## 🚀 Installazione e Utilizzo

### Prerequisiti
```bash
Python 3.7+
pip (gestore pacchetti Python)
```

### Installazione Rapida
```bash
# Clona il repository
git clone <repository-url>
cd darwin_ai

# Setup automatico
make setup

# Avvia la simulazione
make run
```

### Installazione Manuale
```bash
# Crea ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate  # Su macOS/Linux
# .venv\Scripts\activate   # Su Windows

# Installa dipendenze
pip install pygame numpy matplotlib

# Avvia l'applicazione
python main.py
```

## 🎮 Controlli

### Menu Principale
- **↑/↓**: Navigazione tra opzioni
- **←/→**: Modifica valori degli slider
- **Invio/Spazio**: Conferma selezione
- **ESC**: Esci dall'applicazione

### Simulazione
- **ESC**: Vai alle statistiche
- **Spazio**: Pausa/Riprendi
- **V**: Toggle visualizzazione raggi visivi
- **+/-**: Aumenta/Diminuisci velocità
- **↑/↓/←/→**: Muovi camera
- **R**: Reset posizione camera

### Statistiche
- **↑/↓**: Navigazione menu
- **Invio**: Seleziona opzione
- **ESC**: Torna al menu principale

## 🔧 Configurazione

### Parametri Simulazione
- **Numero Prede**: 4-200 individui
- **Numero Predatori**: 2-100 individui
- **Quantità Cibo**: 4-400 unità
- **Durata**: 30-300 secondi
- **Velocità**: 1x-10x velocità normale

### Preset Disponibili
Il progetto include diversi preset predefiniti:
- **Balanced**: Ecosistema equilibrato
- **Predator Dominance**: Predatori dominanti
- **Survival Challenge**: Sfida di sopravvivenza
- **Rapid Evolution**: Evoluzione accelerata
- **Minimal Ecosystem**: Ecosistema minimale

## 📊 Analisi e Report

### Statistiche Disponibili
- **Popolazioni**: Conteggio in tempo reale
- **Sopravvivenza**: Percentuali di sopravvivenza
- **Evoluzione Genetica**: Media dei tratti per specie
- **Riproduzioni**: Numero totale di nuove nascite

### Esportazione Report
I report possono essere esportati in formato HTML con:
- Grafici delle popolazioni nel tempo
- Analisi evolutiva dei genomi
- Radar chart dei tratti genetici
- Statistiche complete della simulazione

## 🏗️ Architettura del Progetto

```
darwin_ai/
├── src/
│   ├── entities/          # Entità del gioco (predatori, prede, cibo)
│   ├── genetics/          # Algoritmi genetici
│   ├── simulation/        # Motore di simulazione
│   ├── ui/               # Interfaccia utente
│   ├── analysis.py       # Analisi avanzate
│   ├── config.py         # Configurazioni
│   ├── presets.py        # Preset predefiniti
│   ├── utils.py          # Utilità
│   └── app.py            # Applicazione principale
├── main.py               # Punto di ingresso
├── requirements.txt      # Dipendenze
├── Makefile             # Comandi di gestione
└── README.md            # Documentazione
```

### Moduli Principali

#### Entities (`src/entities/`)
- `entities.py`: Classi base per tutte le entità
- Implementa predatori, prede e cibo
- Gestisce comportamenti e interazioni

#### Genetics (`src/genetics/`)
- `genetic_algorithm.py`: Implementazione algoritmi genetici
- Crossover, mutazione e selezione
- Gestione genomi specifici per specie

#### Simulation (`src/simulation/`)
- `simulation.py`: Motore principale di simulazione
- Gestisce aggiornamenti, collisioni e statistiche
- Controllo del tempo e delle dinamiche

#### UI (`src/ui/`)
- `screens.py`: Gestione delle schermate
- `components.py`: Componenti UI riutilizzabili
- Navigazione e interazione utente

## 🧪 Principi Scientifici

### Algoritmi Genetici
- **Selezione**: Solo gli individui più adatti si riproducono
- **Crossover**: Combinazione di geni da due genitori
- **Mutazione**: Variazioni casuali per diversità genetica
- **Fitness**: Sopravvivenza e successo riproduttivo

### Dinamiche Ecologiche
- **Relazione Predatore-Preda**: Equilibrio naturale
- **Competizione per Risorse**: Cibo limitato crea pressione selettiva
- **Adattamento**: I tratti vantaggiosi si diffondono nella popolazione
- **Deriva Genetica**: Cambiamenti casuali nelle piccole popolazioni

## 🎯 Obiettivi Educativi

Darwin è progettato per:
- **Visualizzare l'evoluzione**: Osservare la selezione naturale in azione
- **Comprendere la genetica**: Vedere come i tratti si trasmettono
- **Esplorare l'ecologia**: Studiare le interazioni tra specie
- **Imparare la programmazione**: Esempio di design software modulare

## 🚀 Sviluppi Futuri

### Funzionalità Pianificate
- [ ] Più specie e nicchie ecologiche
- [ ] Ambiente dinamico con stagioni
- [ ] Malattie e immunità
- [ ] Migrazione e dispersione
- [ ] Interfaccia web

### Miglioramenti Tecnici
- [ ] Ottimizzazione performance
- [ ] AI avanzata per comportamenti
- [ ] Serializzazione delle simulazioni
- [ ] API per esperimenti automatizzati
- [ ] Testing automatizzato

## 🤝 Contribuire

Contributi benvenuti! Per contribuire:

1. Fork del repository
2. Crea un branch per la tua feature
3. Commit delle modifiche
4. Push al branch
5. Apri una Pull Request

### Aree di Contributo
- Nuove meccaniche evolutive
- Miglioramenti UI/UX
- Ottimizzazioni performance
- Documentazione
- Testing

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per dettagli.

## 🙏 Ringraziamenti

- Pygame community per il framework grafico
- NumPy e Matplotlib per analisi e visualizzazioni
- La comunità scientifica per i principi evolutivi
- Beta testers e contributori

## 📞 Supporto

Per domande, bug reports o suggerimenti:
- Apri un issue su GitHub
- Consulta la documentazione
- Controlla i preset disponibili per esempi

---

*Darwin - Dove l'evoluzione incontra la programmazione* 🧬💻
