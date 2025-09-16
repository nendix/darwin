# Darwin
Darwin è un simulatore di evoluzione 2D che utilizza algoritmi genetici per
simulare l'evoluzione di due specie: predatori e prede. Il progetto dimostra i
principi dell'evoluzione naturale attraverso selezione, riproduzione, mutazione
e adattamento ambientale.

## Funzionamento
Vengono creati randomicamente due pool di specie, prede e predatori che
interagiranno all'interno del mondo della simulazione, avendo come obiettivo
primario la riproduzione.

## Schermate
- **Menu**: Configurazione parametri di simulazione
- **Simulazione**: Visualizzazione in tempo reale
- **Statistiche**: Analisi dettagliate dei risultati

## Analisi e Report

### Statistiche Disponibili
- **Popolazioni**: Conteggio in tempo reale
- **Sopravvivenza**: Percentuali di sopravvivenza
- **Evoluzione Genetica**: Media dei tratti per specie
- **Riproduzioni**: Numero totale di nuove nascite

A fine simulazione c'è la possibilita di esportare dei grafici in formato png

## Genomi delle Specie

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

## Meccaniche di Gioco

### Comportamenti
- **Predatori**: Cacciano le prede, si riproducono
- **Prede**: Evitano i predatori, mangiano cibo, si riproducono

### Sistema Energetico
- **Consumo**: L'energia diminuisce con movimento e tempo
- **Rigenerazione**: Mangiare cibo ripristina l'energia
- **Morte**: Quando finisce l'energai o si viene mangiati

### Riproduzione
- **Soglia**: Punteggio di 100 per potersi riprodurre
- **Crossover**: Combinazione genetica uniforme tra due genitori
- **Mutazione**: Variazioni casuali nei geni della prole

## Installazione
```bash
# Clona il repository
git clone <repository-url>
cd darwin_ai

# Crea il virtual env
make venv

# Attiva il venv
source .venv/bin/activate

# Installa le dipendenze
make deps

# Avvia la simulazione
make run
```

## Sviluppi Futuri

### Funzionalità Pianificate
- [ ] Più specie
- [ ] Aggiunta di nicchie ecologiche(biomi)
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

## Contribuire
Contributi benvenuti! 

Per contribuire:
1. Fork del repository
2. Crea un branch per la tua feature
3. Commit delle modifiche
4. Push al branch
5. Apri una Pull Request
