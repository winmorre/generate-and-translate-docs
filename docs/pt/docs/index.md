# Automatize a tradução de documentos Quick Start

<p align="center">
<a href="#"><img src="img/py_logo.png?sanitize=true" alt="Auto" style="width:20px;height:20px;"></a>
</p>
<p align="center">
<em>Gerenciamento de configuração para Python.</em>
</p>


## Características

 - Inspirado por a **[12-fator inscrição guia](https://12factor.net/config)**
- **Gerenciamento de configurações** (valores padrão, validação, análise, modelagem)
- Proteção de **informações confidenciais** (senhas/tokens)
- Vários **formatos de arquivo** `toml|yaml|json|ini|py` e também carregadores personalizáveis.
- Suporte completo para **variáveis ​​de ambiente** para substituir as configurações existentes (suporte dotenv incluído).
- Sistema opcional em camadas para **ambientes múltiplos** `[padrão, desenvolvimento, teste, produção]` (também chamado de perfis múltiplos)
- Suporte integrado para **Hashicorp Vault** e **Redis** como configurações e armazenamento de segredos.
- Extensões integradas para estruturas da web **Django** e **Flask**.
- **CLI** para operações comuns como `inicializar, listar, escrever, validar, exportar`.

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

## Comandos

Este é um comando `bash`
```bash
echo Hello world!
```

Comando Python Click para imprimir no terminal

```python
import click

click.echo("Hello World")
```

## Leia Mais Links

 > Você posso ler mais sobre Pitão clique [aqui](https://click.palletsprojects.com/en/8.1.x/quickstart/#basic-concepts-creating-a-command)
 > Vocês posso também ler mais cerca de GithubGenericName [aqui](https://github.com)

# Obrigado por ter vindo