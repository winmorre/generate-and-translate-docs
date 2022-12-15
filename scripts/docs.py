import os
import shutil
from typing import Dict, List, Optional, Tuple, Any

import mkdocs.commands.build
import mkdocs.commands.serve
import mkdocs.config
import mkdocs.utils
import typer
import yaml

from translate import *

MKDOCS_NAME = "mkdocs.yml"

DOCS_PATH = Path("docs")

DEFAULT_DOCS_PATH = Path("docs/en")

DEFAULT_CONFIG_PATH: Path = DEFAULT_DOCS_PATH / MKDOCS_NAME

missing_translation_snippet = """
<div style="border-color: #bea925;border: 0.05rem solid #bea925;border-radius: 0.2rem;
box-shadow: 0 0.2rem 0.5rem rgba(0,0,0,.2),0 0 0.05rem rgba(0,0,0,.1);display: flow-root;font-size: .64rem;
margin: 1.5625em 0; padding: 0 0.6rem;page-break-inside: avoid;"> 
<p style="background-color: #be6725;color: #be2525"> <span style="color: #be2525">&#9888;</span> Warning </p>
<p>The current page still doesn't have a translation for this language.</p>
<p> But you can help translating it: <a href="https://github.com/dynaconf/dynaconf/blob/9f91e0dc1c96c9dcbc2feca6bd29f898a157b9a9/CONTRIBUTING.md" target="_blank">Contributing</a></p>
</div>
"""


def get_en_config() -> dict:
    return mkdocs.utils.yaml_load(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))


def get_lang_paths():
    return sorted(DOCS_PATH.iterdir())


def lang_callback(lng_code: Optional[str]):
    if lng_code is None:
        return

    if not lng_code.isalpha() or len(lng_code) > 2:
        typer.echo("Use a 2 letter language code, like: es, pt,fr,sn")
        raise typer.Abort()
    return lng_code


def complete_existing_lang(incomplete: str):
    lng_path: Path
    for lng_path in get_lang_paths():
        if lng_path.is_dir() and lng_path.name.startswith(incomplete):
            yield lng_path.name


def get_base_lang_config(lng_code: str):
    en_config = get_en_config()
    dynaconf_url_base = "https://dynaconf.com/"
    new_config = en_config.copy()
    new_config["site_url"] = en_config["site_url"] + f"{lng_code}/"
    new_config["theme"]["logo"] = dynaconf_url_base + en_config["theme"]["logo"]
    new_config["theme"]["favicon"] = dynaconf_url_base + en_config["theme"]["favicon"]
    new_config["theme"]["language"] = lng_code
    new_config["theme"]["locale"] = lng_code
    new_config["nav"] = en_config["nav"][:2]

    return new_config


def create_new_files(filenames: List[str | None], new_config_docs_path: Path, lng_code: str) -> None:
    if len(filenames) == 0:
        default_index_page_path = DEFAULT_DOCS_PATH / "docs" / "index.md"
        new_index_path: Path = new_config_docs_path / "index.md"
        default_index_content = default_index_page_path.read_text(encoding="utf-8")
        translate_file_content(output_path=new_index_path, content=default_index_content, lng_code=lng_code)
    else:
        for name in filenames:
            default_page_file_path = DEFAULT_DOCS_PATH / "docs" / str(name)
            new_page_file_path = new_config_docs_path / str(name)
            default_file_content = default_page_file_path.read_text(encoding="utf-8")
            translate_file_content(output_path=new_page_file_path, content=default_file_content, lng_code=lng_code)

        typer.echo(f"New files created for {','.join(filenames)}")


def get_all_md_filenames():
    path = DEFAULT_DOCS_PATH / "docs"
    absolute_path = os.path.abspath(path).split("/scripts")
    absolute_path = "".join(absolute_path)

    filenames = next(os.walk(str(absolute_path)), (None, None, []))[2]

    return filenames


def remove_and_copytree(build_lang_path, language_path):
    shutil.rmtree(build_lang_path, ignore_errors=True)
    shutil.copytree(language_path, build_lang_path)


def build_paths(lng_code: str) -> Tuple[Path, ...]:
    lang_path: Path = Path("docs") / lng_code
    if not lang_path.is_dir():
        typer.echo(f"The language translation doesn't seem to exist yet: {lng_code}")
        raise typer.Abort()
    typer.echo(f"Building docs for: {lng_code}")
    build_dir_path = Path("docs_build")
    build_dir_path.mkdir(exist_ok=True)
    build_lang_path = build_dir_path / lng_code
    site_path = Path("site").absolute()
    if lng_code == "en":
        dist_path = site_path
    else:
        dist_path: Path = site_path / lng_code

    return build_lang_path, dist_path, lang_path


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


def generate_key_to_section(
        file_to_nav: Dict[str, Tuple[str, ...]],
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


def update_use_lng_file_to_nav(language_nav: List,
                               file_to_nav: Dict[str, Tuple[str, ...]],
                               build_lng_path: Path) -> Dict[str, Tuple[str, ...]]:
    use_lng_file_to_nav = get_file_to_nav_map(language_nav[2:])

    for file in file_to_nav:
        file_path = Path(file)
        lang_file_path: Path = build_lng_path / "docs" / file_path
        en_file_path: Path = DEFAULT_DOCS_PATH / "docs" / file_path
        lang_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not lang_file_path.is_file():
            default_text = en_file_path.read_text(encoding="utf-8")
            lang_file_path.write_text(default_text, encoding="utf-8")
            file_key = file_to_nav[file]
            use_lng_file_to_nav[file] = file_key

    return use_lng_file_to_nav


def save_new_lng_nav(lng_config, lng_nav, nav, new_nav, build_lng_path):
    export_lang_nav = [lng_nav[0], nav[1]] + new_nav
    lng_config["nav"] = export_lang_nav
    build_lang_config_path: Path = build_lng_path / MKDOCS_NAME
    build_lang_config_path.write_text(
        yaml.dump(lng_config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )


def load_lng_nav_and_en_nav(lng_path: Path) -> Tuple:
    en_lang_config_path: Path = DEFAULT_DOCS_PATH / MKDOCS_NAME
    en_config: dict = mkdocs.utils.yaml_load(en_lang_config_path.read_text(encoding="utf-8"))
    nav = en_config["nav"]
    lang_config_path: Path = lng_path / MKDOCS_NAME
    lang_config: dict = mkdocs.utils.yaml_load(
        lang_config_path.read_text(encoding="utf-8")
    )

    return nav, lang_config


def update_single_lng(lng_code: str):
    lang_path = DOCS_PATH / lng_code
    typer.echo(f"Updating {lang_path.name}")
    update_config(lang_path.name)


def translate_navs(lng_code: str):
    lng_path = DOCS_PATH / lng_code
    config_path = lng_path / MKDOCS_NAME

    config: dict = mkdocs.utils.yaml_load(config_path.read_text(encoding="utf-8"))

    navs = config["nav"]
    new_nav = []

    for n in navs:
        for k, v in n.items():
            new_key = translation(text=k, dest_lng=lng_code)
            new_nav.append({new_key: v})

    config["nav"] = new_nav

    config_path.write_text(
        yaml.dump(config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )
    typer.echo("Navs translated successfully")


def update_config(lng_code: str):
    lng_path: Path = DOCS_PATH / lng_code
    config_path = lng_path / MKDOCS_NAME
    current_config: dict = mkdocs.utils.yaml_load(
        config_path.read_text(encoding="utf-8")
    )
    if lng_code == "en":
        config = get_en_config()
    else:
        config = get_base_lang_config(lng_code)
        config["nav"] = current_config["nav"]
        config["theme"]["language"] = current_config["theme"]["language"]
    languages = [{"en": "/"}]
    alternate: List[Dict[str, str]] = config["extra"].get("alternate", [])
    alternate_dict = {alt["link"]: alt["name"] for alt in alternate}
    new_alternate: List[Dict[str, str]] = []
    for lang_path in get_lang_paths():
        if lang_path.name == "en" or not lang_path.is_dir():
            continue
        name = lang_path.name
        languages.append({name: f"/{name}/"})
    for lang_dict in languages:
        name = list(lang_dict.keys())[0]
        url = lang_dict[name]
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


def get_sections(nav: list) -> Dict[Tuple[str, ...], str]:
    sections: Dict[Tuple[str, ...], str] = {}

    for i in nav:
        for k, v in i.items():
            sections[v] = (k,)
    return sections
