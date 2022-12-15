# Automatizza la traduzione di documenti Avvio rapido

<p align="center">
<a href="#"><img src="img/py_logo.png?sanitize=true" alt="Auto" style="width:20px;height:20px;"></a>
</p>
<p align="center">
<em>Gestione della configurazione per Python.</em>
</p>


## Caratteristiche

 - Ispirato di il **[fattore 12 applicazione guida](https://12factor.net/config)**
- **Gestione delle impostazioni** (valori predefiniti, convalida, analisi, creazione di modelli)
- Protezione delle **informazioni sensibili** (password/token)
- Più **formati di file** `toml|yaml|json|ini|py` e caricatori personalizzabili.
- Pieno supporto per le **variabili d'ambiente** per sovrascrivere le impostazioni esistenti (supporto dotenv incluso).
- Sistema a più livelli opzionale per **ambienti multipli** "[predefinito, sviluppo, test, produzione]" (chiamato anche multiprofili)
- Supporto integrato per **Hashicorp Vault** e **Redis** come archiviazione di impostazioni e segreti.
- Estensioni integrate per framework web **Django** e **Flask**.
- **CLI** per operazioni comuni come `init, list, write, validate, export`.

## TOML
 ```toml
[default]
key = "value"
a_boolean = false
number = 1234

[development]
key = "development value"
SQLALCHEMY_DB_URI = "sqlite://data.db"

[production]
key = "production value"
SQLALCHEMY_DB_URI = "postgresql://..."
```

## Comandi

Questo è un comando `bash`
```bash
echo Hello world!
```

Python Fare clic sul comando per stampare nel terminale

```python
import click

click.echo("Hello World")
```

## Leggi altri link

 > Voi Potere leggere Di più Su pitone clic [qui](https://click.palletsprojects.com/en/8.1.x/quickstart/#basic-concepts-creating-a-command)
 > Voi Potere anche leggere Di più di Github [qui](https://github.com)

# Grazie per essere venuto