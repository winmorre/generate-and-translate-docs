# Автоматизирайте превода на документи Бърз старт

<p align="center">
<a href="#"><img src="img/py_logo.png?sanitize=true" alt="Авто" style="width:20px;height:20px;"></a>
</p>
<p align="center">
<em>Управление на конфигурацията за Python.</em>
</p>


## Характеристика

 - Вдъхновен от на **[12-фактор приложение ръководство](https://12factor.net/config)**
- **Управление на настройките** (стойности по подразбиране, валидиране, анализиране, шаблониране)
- Защита на **чувствителна информация** (пароли/токени)
- Множество **файлови формати** `toml|yaml|json|ini|py` и също персонализируеми зареждащи програми.
- Пълна поддръжка за **променливи на средата** за отмяна на съществуващи настройки (включена поддръжка на dotenv).
- Допълнителна многопластова система за **много среди** `[по подразбиране, разработка, тестване, производство]` (наричани още много профили)
- Вградена поддръжка за **Hashicorp Vault** и **Redis** като настройки и съхранение на тайни.
- Вградени разширения за **Django** и **Flask** уеб рамки.
- **CLI** за общи операции като `init, list, write, validate, export`.

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

## Команди

Това е команда `bash`
```bash
echo Hello world!
```

Python Click команда за печат в терминала

```python
import click

click.echo("Hello World")
```

## Прочетете още връзки

 > Ти мога Прочети Повече ▼ На питон щракнете [тук](https://click.palletsprojects.com/en/8.1.x/quickstart/#basic-concepts-creating-a-command)
 > Ти мога също Прочети Повече ▼ относно Github [тук](https://github.com)

# Благодаря, че дойдохте