import shutil
from typing import Dict, List, Optional, Tuple, Any

import click
import yaml
from mkdocs import utils

from .translate import *

MKDOCS_FILE_NAME = "mkdocs.yml"
DOCS_PATH = Path("docs")

DEFAULT_DOCS_PATH = Path("docs/en")

DEFAULT_DOCS_CONFIG_PATH = DEFAULT_DOCS_PATH / MKDOCS_FILE_NAME


def get_default_docs_config() -> Dict:
    return utils.yaml_load(DEFAULT_DOCS_CONFIG_PATH.read_text(encoding="utf-8"))


def get_lng_paths():
    return sorted(DOCS_PATH.iterdir())


def complete_existing_language(incomplete: str) -> Optional[str]:
    language_path: Path
    for language_path in get_lng_paths():
        if language_path.is_dir() and language_path.name.startswith(incomplete):
            yield language_path.name


def get_default_language_configs(lng_code: str) -> Dict[str, Any]:
    default_config = get_default_docs_config()
    url_base = "https://docs.com/"

    new_config = default_config.copy()
    new_config["site_url"] = default_config["site_url"] + f"{lng_code}/"
    new_config["theme"]["logo"] = url_base + default_config["theme"]["logo"]
    new_config["theme"]["favicon"] = default_config["theme"]["favicon"]
    new_config["theme"]["language"] = lng_code
    new_config["theme"]["locale"] = lng_code
    new_config["nav"] = default_config["nav"][:2]

    config_plugins = default_config["plugins"]
    for p in config_plugins:
        if type(p) is dict and "search" in p:
            p["search"]["lang"] = lng_code

    new_config["plugins"] = config_plugins

    return new_config


def remove_and_copytree(build_lang_path, language_path):
    shutil.rmtree(build_lang_path, ignore_errors=True)
    shutil.copytree(language_path, build_lang_path)


def build_paths(lng_code: str) -> Tuple[Path, ...]:
    lng_path: Path = DOCS_PATH / lng_code
    if not lng_path.is_dir():
        click.echo(f"The language translation doesn't seem to exist yet:  {lng_code}")
        raise click.Abort()

    click.echo(f"Building docs for: {lng_code}")
    build_dir_path = Path("docs_build")
    build_dir_path.mkdir(exist_ok=True)
    build_lng_path = build_dir_path / lng_code
    site_path = Path("site").absolute()

    if lng_code == "en":
        dist_path: Path = site_path
    else:
        dist_path: Path = site_path / lng_code

    return build_lng_path, dist_path, lng_path


def update_new_lng_nav(key_to_section: Dict[Tuple, List]) -> List[Dict[str, Any]]:
    new_nav = []

    for i in key_to_section[()]:
        for k, v in i.items():
            if type(v) is list and len(v) == 1:
                new_nav.append({k: v[0]})
            elif type(v) is list and len(v) > 1:
                new_nav.append({k: v})
            elif type(v) is str:
                new_nav.append({k: v})

    return new_nav


def generate_key_to_section(file_to_nav: Dict[str, Tuple[str, ...]],
                            use_lng_file_to_nav: Dict[str, Tuple[str, ...]]) -> Dict[Tuple, List]:
    key_to_section = {(): []}

    for file, orig_file_key in file_to_nav.items():
        if file in use_lng_file_to_nav:
            file_key = use_lng_file_to_nav[file]
        else:
            file_key = orig_file_key
        section = get_key_section(key_to_section=key_to_section, key=file_key)
        section.append(file)

    return key_to_section


def update_use_lng_file_to_nav(
        lng_nav: List, file_to_nav: Dict[str, Tuple[str, ...]], build_lng_path: Path, lng_code: str
) -> Dict[str, Tuple[str, ...]]:
    use_lng_file_to_nav = get_file_to_nav_map(lng_nav[2:])

    for file in file_to_nav:
        file_path = Path(file)

        lng_file_path: Path = build_lng_path / "docs" / file_path
        default_file_path: Path = DEFAULT_DOCS_PATH / "docs" / file_path
        lng_file_path.parent.mkdir(parents=True, exist_ok=True)

        if not lng_file_path.is_file():
            default_lng_text = default_file_path.read_text(encoding="utf-8")
            # Translate default content to new language
            translate_file_content(output_path=lng_file_path, content=default_lng_text, lng_code=lng_code)
            file_key = file_to_nav[file]
            use_lng_file_to_nav[file] = file_key
    return use_lng_file_to_nav


def save_new_lang_nav(lng_config, lng_nav, nav, new_nav, build_lng_path, lng_code: str):
    export_lng_nav = [lng_nav[0], nav[1]] + new_nav

    lng_config["nav"] = export_lng_nav

    build_lng_config_path: Path = build_lng_path / MKDOCS_FILE_NAME
    build_lng_config_path.write_text(
        yaml.dump(lng_config, sort_keys=False, width=200, allow_unicode=True)
    )


def load_lang_nav_and_default_lng_nav(lng_path: Path) -> Tuple[List, Dict[str, Any]]:
    default_lng_config_path: Path = DEFAULT_DOCS_PATH / MKDOCS_FILE_NAME
    default_config: Dict = utils.yaml_load(default_lng_config_path.read_text(encoding="utf-8"))
    nav = default_config["nav"]
    lng_config_path: Path = lng_path / MKDOCS_FILE_NAME
    lng_config: Dict = utils.yaml_load(lng_config_path.read_text(encoding="utf-8"))

    return nav, lng_config


def update_config(lng_code: str):
    lng_path: Path = DOCS_PATH / lng_code
    config_path: Path = lng_path / MKDOCS_FILE_NAME
    current_config: Dict = utils.yaml_load(config_path.read_text(encoding="utf-8"))

    if lng_code == "en":
        config = get_default_docs_config()
    else:
        config = get_default_language_configs(lng_code)
        config["nav"] = current_config["nav"]
        config["theme"]["language"] = current_config["theme"]["language"]
    languages = [{"en": "/"}]
    alternate: List[Dict[str, str]] = config["extra"].get("alternate", [])
    alternate_dict = {alt["link"]: alt["name"] for alt in alternate}
    new_alternate: List[Dict[str, str]] = []
    for lng_path in get_lng_paths():
        if lng_path.name == "en" or not lng_path.is_dir():
            continue
        name = lng_path.name
        languages.append({name: f"/{name}/"})

    for lng_dict in languages:
        name = list(lng_dict.keys())[0]
        url = lng_dict[name]

        if url not in alternate_dict:
            new_alternate.append({"link": url, "name": name})
        else:
            use_name = alternate_dict[url]
            new_alternate.append({"link": url, "name": use_name})

        config["nav"][1] = {"Languages": languages}
        config["extra"]["alternate"] = new_alternate

        config_path.write_text(
            yaml.dump(config, sort_keys=False, width=200, allow_unicode=True),
            encoding="utf-8",
        )


def get_key_section(
        *, key_to_section: Dict[Tuple[str, ...], list], key: Tuple[str, ...]
) -> list:
    if key in key_to_section:
        return key_to_section[key]
    super_key = key[:-1]
    title = key[-1]
    super_section = get_key_section(key_to_section=key_to_section, key=super_key)
    new_section = []
    super_section.append({title: new_section})
    key_to_section[key] = new_section
    return new_section


def get_file_to_nav_map(nav: list) -> Dict[str, Tuple[str, ...]]:
    file_to_nav = {}
    for item in nav:
        if type(item) is str:
            file_to_nav[item] = tuple()
        elif type(item) is dict:
            item_key = list(item.keys())[0]
            sub_nav = item[item_key]
            sub_file_to_nav = get_file_to_nav_map(sub_nav)
            for k, v in sub_file_to_nav.items():
                file_to_nav[k] = (item_key,) + v
    return file_to_nav


def get_file_to_navigate_to_as_map(nav: list) -> Dict[str, Tuple[str, ...]]:
    file_to_nav = {}

    for i in nav:
        for k, v in i.items():
            file_to_nav[v] = (k,)

    return file_to_nav


def get_sections(nav: list):
    sections = {}

    for i in nav:
        for k, v in i.items():
            sections[v] = (k,)
    return sections


def update_single_lang(lang: str):
    lang_path = DOCS_PATH / lang
    click.echo(f"Updating {lang_path.name}")
    update_config(lang_path.name)


def update_languages(
        lng_code: str | None
):
    """
    Update the mkdocs.yml file Languages section including all the available languages.
    The LANG argument is a 2-letter language code. If it's not provided, update all the
    mkdocs.yml files (for all the languages).
    """
    if lng_code is None:
        for lang_path in get_lng_paths():
            if lang_path.is_dir():
                update_single_lang(lang_path.name)
    else:
        update_single_lang(lng_code)
