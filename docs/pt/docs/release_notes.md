# Notas de Lançamento

Esta versão é mais sobre correções de bugs e melhorias,

Idealmente, as bibliotecas fornecidas serão atualizadas sob demanda somente quando uma nova segurança
ou correção de bug importante é lançada no respectivo repositório fornecido.


### Interpolação de variáveis

O mecanismo para avaliar valores `Lazy` foi refatorado e agora `@format` e
Os valores `@jinja` podem ser usados ​​em dicionários e listas em qualquer nível de aninhamento.


```py

def my_function(name):
    return f"this is computed during validation time for {name} "

```

Historicamente, o Project Docs trabalhou em ambientes multicamadas para
carregando dados de arquivos, então você deveria ter um arquivo como:

```toml
[default]
key = 'value'

[production]
key = 'value'
```

## Chegando em 0.1.1
- Suporte para Pydantic BaseSettings para validadores.
- Suporte para substituição do analisador `toml` no carregador de envvars.