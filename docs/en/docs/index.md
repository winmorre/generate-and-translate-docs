# Automate docs translation Quick Start

<p align="center">
  <a href="https://dynaconf.com"><img src="img/logo_400.svg?sanitize=true" alt="Dynaconf"></a>
</p>
<p align="center">
    <em>Configuration Management for Python.</em>
</p>

<p align="center"><a href="/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat-square"></a> <a href="https://pypi.python.org/pypi/dynaconf"><img alt="PyPI" src="https://img.shields.io/pypi/v/dynaconf.svg"></a><a href="https://github.com/dynaconf/dynaconf/actions/workflows/main.yml"><img src="https://github.com/dynaconf/dynaconf/actions/workflows/main.yml/badge.svg"></a><a href="https://codecov.io/gh/dynaconf/dynaconf"><img alt="codecov" src="https://codecov.io/gh/dynaconf/dynaconf/branch/master/graph/badge.svg"></a> <a href="https://www.codacy.com/gh/dynaconf/dynaconf/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dynaconf/dynaconf&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/3fb2de98464442f99a7663181803b400"/></a> <img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/dynaconf/dynaconf.svg"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/dynaconf/dynaconf.svg"> <a href="https://github.com/dynaconf/dynaconf/discussions"><img alt="Discussions" src="https://img.shields.io/badge/discussions-forum-yellow.svg?logo=googlechat"></a></p>

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

