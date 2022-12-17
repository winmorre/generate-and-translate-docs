## Automate Project Docs translation using Python

### Description

This project is about translation of project Docs to multiple languages. 
Project Docs are mostly create initially in one language the team agrees on.Large distributed teams may have the need to translate this documentation for readers.
This can be a tedious task for developers. Now with this project, developers can easily and quickly generate and translate these Docs in other languages using the command line or running the scripts in this repo.

This project makes use of [Mkdocs ](https://www.mkdocs.org/getting-started/) to create the project documentation

### Get started

* Create a virtual environment
```py
    python -m venv venv-name
```

* Activate Virtual environment
```bash
    source venv-name/bin/ativate
```

### Generate new docs project
Use mkdocs command below to generate a new project.
```python
mkdocs new .
```

Your current project structure should like this
```toml
 docs\
    index.md
mkdocs.yml
```

Create a folder for the default langauge for your project. the folder name should the ISO-639 code for the chosen default langauge. 
In this case you can use `en` which is the ISO-639 code for English.

Your project structure should now like this
```toml
docs/
    en/
        docs/
            index.md
            ...
        mkdocs.yml
```

### Project commands

> Running the code below will create a new language translation document.

```py
    python ./scripts/cli.py new-lng "your-language-code" 
```

> To build the document(s) generated for a single language, you can run the below command:

```py
    python ./scripts/cli.py build-lng "your-language-code"
```

> To build all the documents generated for all languages supported in you project, run the below command 

```py
python ./scripts/cli.py build-all 
```

> To serve the built docs, run the below command
```py
python ./scripts/cli.py serve
```

> To serve docs for s single language, use the command below
```py
python ./scripts/cli.py live "your-language-to-serve"
```


### Project dependencies

* mkdocs
* click
* typer
* googletrans==3.1.0a0