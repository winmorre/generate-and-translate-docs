# Note di rilascio

Questa versione riguarda più correzioni di bug e miglioramenti,

Idealmente le librerie fornite verranno aggiornate su richiesta solo quando una nuova sicurezza
o un'importante correzione di bug viene rilasciata sul rispettivo repository fornito.


### Interpolazione variabile

Il meccanismo per valutare i valori "Lazy" è stato rifattorizzato e ora "@format" e
I valori `@jinja` possono essere utilizzati all'interno di dizionari ed elenchi in qualsiasi livello di annidamento.


```py

def my_function(name):
    return f"this is computed during validation time for {name} "

```

Storicamente Project Docs ha funzionato in ambienti a più livelli per
caricamento di dati da file, quindi avresti dovuto avere un file come:

```toml
[default]
key = 'value'

[production]
key = 'value'
```

## In arrivo nella versione 0.1.1
- Supporto per Pydantic BaseSettings per i validatori.
- Supporto per la sostituzione del parser `toml` su envvars loader.