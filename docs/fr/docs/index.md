# Automatiser la traduction des documents Démarrage rapide

<p align="center">
<a href="#"><img src="img/py_logo.png?sanitize=true" alt="Auto" style="width:20px;height:20px;"></a>
</p>
<p align="center">
<em>Gestion de la configuration pour Python.</em>
</p>


## Fonctionnalités

 - Inspiré par la **[12 facteurs application guide](https://12factor.net/config)**
- **Gestion des paramètres** (valeurs par défaut, validation, parsing, template)
- Protection des **informations sensibles** (mots de passe/tokens)
- Plusieurs **formats de fichiers** `toml|yaml|json|ini|py` et également des chargeurs personnalisables.
- Prise en charge complète des **variables d'environnement** pour remplacer les paramètres existants (prise en charge dotenv incluse).
- Système en couches optionnel pour **multi environnements** `[default, development, testing, production]` (également appelé multi profiles)
- Prise en charge intégrée de **Hashicorp Vault** et **Redis** en tant que paramètres et stockage de secrets.
- Extensions intégrées pour les frameworks Web **Django** et **Flask**.
- **CLI** pour les opérations courantes telles que `init, list, write, validate, export`.

##TOML
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

## Commandes

Ceci est une commande `bash`
```bash
echo Hello world!
```

Python Cliquez sur la commande pour imprimer dans le terminal

```python
import click

click.echo("Hello World")
```

## Lire plus de liens

 > Tu boîte lis Suite sur python Cliquez sur [ici](https://click.palletsprojects.com/en/8.1.x/quickstart/#basic-concepts-creating-a-command)
 > Tu boîte aussi lis Suite sur GithubGenericName [ici](https://github.com)

# Merci d'être venu