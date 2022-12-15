# Release Notes

Kuburitswa uku kune zvakawanda nezve bug kugadzirisa uye kuvandudzwa,

Nenzira yakanaka, maraibhurari anotengeswa anokwidziridzwa pakudiwa chete kana chengetedzo nyowani
kana yakakosha bug gadziriso inoburitswa pane inotengeswa inotengeswa repository.


### Kududzira kwakasiyana

Muchina wekuongorora `Simbe` wadzokororwa uye ikozvino `@format` uye
`@jinja` kukosha kunogona kushandiswa mukati meduramazwi uye zvinyorwa mune chero mazinga ekugara.


```py

def my_function(name):
    return f"this is computed during validation time for {name} "

```

Nhoroondo Project Docs yakashanda munzvimbo dzakasiyana siyana dze
kurodha data kubva kumafaira, saka waifanirwa kuve nefaira rakaita se:

```toml
[default]
key = 'value'

[production]
key = 'value'
```

## Kuuya mukati 0.1.1
- Tsigiro yePydantic BaseSettings yeValidators.
- Tsigiro yekutsiva `toml` parser pane envvars loader.