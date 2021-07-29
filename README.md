# ScrapeItalianNewspapers
Script in python che scarica, da una data ad un'altra, un sample a scelta di articoli dai siti di sei quotidiani italiani.

## Istruzioni per l'installazione
Per utilizzare lo script, installare le dipendenze:
```
bs4==0.0.1
beautifulsoup4==4.9.3
requests==2.25.1
newspaper3k==0.2.8
nltk==3.6.2
```
può essere fatto installandole direttamente da requirements.txt:

```
python pip install -r requirements.txt
```
## Utilizzo
Lo script funziona da riga di comando. I sei quotidiani su cui funziona sono commentati all'inizio del codice.

Innanzitutto, richiede di inserire l'url del sito web del quotidiano, nella forma: _sitoweb_.it
Subito dopo, vanno specificate le date da cui (e fino a cui) selezionare e scaricare i link, nella forma _AAAAMMGG_.
Tramite Wayback CDX server (https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) viene generata una lista di tutti gli screenshot di quel sito nel periodo selezionato, e successivamente da ogni screenshot delle home page estratti tutti i link degli articoli e suddivisi per anno. Viene creato anche un file csv di backup al termine della raccolta dei link, con tutti i link salvati e suddivisi per anno.
Il processo di reperimento dei link potrebbe prendere anche qualche ora, se si decide di prendere in considerazione più anni.
