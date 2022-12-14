# Automate docs translation Quick Start

<p align="center">
  <a href="#"><img src="img/py_logo.png?sanitize=true" alt="Auto" style="width:20px;height:20px;"></a>
</p>
<p align="center">
    <em>Configuration Management for Python.</em>
</p>


## Features

- Inspired by the **[12-factor application guide](https://12factor.net/config)**
- **Settings management** (default values, validation, parsing, templating)
- Protection of **sensitive information** (passwords/tokens)
- Multiple **file formats** `toml|yaml|json|ini|py` and also customizable loaders.
- Full support for **environment variables** to override existing settings (dotenv support included).
- Optional layered system for **multi environments** `[default, development, testing, production]` (also called multi profiles)
- Built-in support for **Hashicorp Vault** and **Redis** as settings and secrets storage.
- Built-in extensions for **Django** and **Flask** web frameworks.
- **CLI** for common operations such as `init, list, write, validate, export`.

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

## Commands

This is a `bash` command
```bash
echo Hello world!
```

Python Click command to print in terminal

```python
import click

click.echo("Hello World")
```

## Read More Links

> You can read more on python click [here](https://click.palletsprojects.com/en/8.1.x/quickstart/#basic-concepts-creating-a-command)
> YOu can also read more about Github [here](https://github.com)

# Thanks for coming around