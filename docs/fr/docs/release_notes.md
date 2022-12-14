# Notes de version

Cette version concerne davantage les corrections de bogues et les améliorations,

Idéalement, les bibliothèques fournies seront mises à niveau à la demande uniquement lorsqu'une nouvelle sécurité
ou un correctif de bogue important est publié sur le référentiel du fournisseur respectif.


### Interpolation de variables

Le mécanisme d'évaluation des valeurs `Lazy` a été refactorisé et maintenant `@format` et
Les valeurs `@jinja` peuvent être utilisées dans les dictionnaires et les listes à tous les niveaux d'imbrication.


```py

def my_function(name):
    return f"this is computed during validation time for {name} "

```

Historiquement, Project Docs fonctionnait dans des environnements multicouches pour
charger des données à partir de fichiers, vous étiez donc censé avoir un fichier comme:

```toml
[default]
key = 'value'

[production]
key = 'value'
```

## À venir dans la 0.1.1
- Prise en charge de Pydantic BaseSettings pour les validateurs.
- Prise en charge du remplacement de l'analyseur `toml` sur le chargeur envvars.