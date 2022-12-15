# Otomatiki magwaro ekushandura Kurumidza Kutanga

<p align="center">
<a href="#"><img src="img/py_logo.png?sanitize=true" alt="Auto" style="width:20px;height:20px;"></a>
</ p>
<p align="center">
<em>Kuronga Kwekugadzirisa kwePython.</em>
</ p>


## Zvimiro

 - Kufemerwa by the **[12-chinhu application gwara](https://12factor.net/config)**
- ** Settings manejimendi ** (default value, kusimbiswa, kupatsanura, template)
-Kudzivirirwa kwe** ruzivo rwakadzama ** (mapassword / tokens)
-Akawanda **mafaira mafomati** `toml|yaml|json|ini|py` uye zvakare customizable loaders.
-Rutsigiro rwakakwana rwe **zvakatipoteredza zvinosiyana** kupfuudza zvigadziriso zviripo (rutsigiro rwedotenv runosanganisirwa).
-Inosarudzika yakaturikidzana sisitimu ye ** yakawanda nharaunda ** `[default, kusimudzira, kuyedza, kugadzira]` (inonziwo akawanda profiles)
-Yakavakirwa-mukati rutsigiro rwe ** Hashicorp Vault ** uye ** Redis ** sezvirongwa uye zvakavanzika zvekuchengetedza.
-Yakavakirwa-mukati mawedzero e **Django** uye **Flask** webhu masisitimu.
- ** CLI ** yezvakajairika mashandiro akadai `init, rondedzero, nyora, simbisa, kutumira kunze`.

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

## Mirairo

Uyu murairo we `bash`
```bash
echo Hello world!
```

Python Dzvanya kuraira kuti udhinde mune terminal

```python
import click

click.echo("Hello World")
```

## Verenga Zvimwe Zvisungo

 > Iwe anogona verenga zvimwe on python tinya [pano](https://click.palletsprojects.com/en/8.1.x/quickstart/#basic-concepts-creating-a-command)
 > IWE anogona wo verenga zvimwe nezve Github [pano](https://github.com)

# Maita basa nekuuya