import os
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Pool

from mkdocs.commands.serve import serve

from .docs import *


@click.group(name="docs-cli")
def cli():
    pass


@cli.command(name="new-lng")
@click.argument("lng-code")
def new_lng(lng_code: str):
    """
    Generate a new docs translation directory for the language LANG.
    lng-code should be a 2  letter language code, like: en, es, de, pt, etc.
    """

    new_path: Path = DOCS_PATH / lng_code
    if new_path.exists():
        click.echo(f"The language already exist: {lng_code}")
        raise click.Abort

    new_path.mkdir()
    new_config: Dict[str, Any] = get_default_language_configs(lng_code=lng_code)
    new_config_path: Path = Path(new_path) / MKDOCS_FILE_NAME

    lng_nav = new_config["nav"]

    translated_export_lng_nav = []

    for n in lng_nav:
        for k, v in n.items():
            translated_key = translation(text=k, dest_lng=lng_code)
            translated_export_lng_nav.append({translated_key: v})

    new_config["nav"] = translated_export_lng_nav
    new_config["site_description"] = translation(text=new_config["site_description"], dest_lng=lng_code)

    new_config_path.write_text(
        yaml.dump(new_config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )

    new_config_docs_path = new_path / "docs"
    new_config_docs_path.mkdir()

    default_file_names = get_all_md_filenames()
    create_new_files(filenames=default_file_names,new_config_docs_path=new_config_docs_path,lng_code=lng_code)

    # copy image files to new location
    shutil.copytree(DEFAULT_DOCS_PATH / "docs" / "img", new_config_docs_path / "img")
    new_overrides_gitignore_path = new_path / "overrides" / ".gitignore"
    new_overrides_gitignore_path.parent.mkdir(parents=True, exist_ok=True)
    new_overrides_gitignore_path.write_text("")

    click.secho(f"Successfully initialized: {new_path}", color=True)
    update_languages(lng_code=None)


@cli.command()
@click.argument("lng-code")
def build_lng(lng_code: str):
    """
    Build the docs for a langauge, filling missing pages with translation notification
    lng-code is 2-letter Language code something like es,en,pt
    """

    build_lng_path, dist_path, lng_path = build_paths(lng_code=lng_code)
    remove_and_copytree(build_lng_path, lng_path)

    nav, lng_config = load_lang_nav_and_default_lng_nav(lng_path=lng_path)
    lng_nav = lng_config["nav"]

    file_to_nav = get_file_to_navigate_to_as_map(nav=nav[2:])

    use_lng_file_to_nav = update_use_lng_file_to_nav(
        lng_nav=lng_nav,
        file_to_nav=file_to_nav,
        build_lng_path=build_lng_path,
    )

    key_to_section = generate_key_to_section(file_to_nav=file_to_nav, use_lng_file_to_nav=use_lng_file_to_nav)
    new_nav = update_new_lng_nav(key_to_section=key_to_section)

    save_new_lang_nav(
        lng_config=lng_config,
        lng_nav=lng_nav,
        nav=nav,
        new_nav=new_nav,
        build_lng_path=build_lng_path,
        lng_code=lng_code,
    )

    current_dir = os.getcwd()
    os.chdir(build_lng_path)
    subprocess.run(["mkdocs", "build", "--site-dir", "--clean"], check=True)
    os.chdir(current_dir)
    click.secho(f"Successfully built docs for: {lng_code}")


@cli.command(name="build-all")
def build_all():
    """
    Build mkdocs site for en and then build each language inside, end result is located at directory ./site/
    with each language inside
    """
    site_path = Path("site").absolute()
    update_languages(lng_code=None)
    current_dir = os.getcwd()
    os.chdir(DEFAULT_DOCS_PATH)
    click.echo("Building docs for: en")
    subprocess.run(["mkdocs", "build", "--site-dir", site_path], check=True)
    os.chdir(current_dir)

    lngs = []
    for lng in get_lng_paths():
        if lng == DEFAULT_DOCS_PATH or not lng.is_dir():
            continue
        lngs.append(lng.name)
    cpu_count = os.cpu_count() or 1
    with Pool(cpu_count * 2) as p:
        p.map(build_lng, lngs)


@cli.command()
def serve():
    """
    A quick server to preview a built site with translations.
    For development, prefer the command live (or just mkdocs serve).
    This is here only to preview a site with translations already built.
    Make sure you run the build-all command first.
    """
    click.echo("Warning: this is a very simpler server")
    click.echo("For development, use the command live instead")
    click.echo("This is here only to preview a ite with translations already built")
    click.echo("Make sure you run the build-all command first.")
    os.chdir("site")

    server_address = ("", 8009)
    server = HTTPServer(server_address, SimpleHTTPRequestHandler)
    click.echo(f"Serving at http://127.0.0.1:8009")
    server.serve_forever()


@cli.command()
@click.option("--lng-code", help="2-letter Language code something like es,en,pt")
def live(lng_code: str):
    """
    Serve with livereload a docs site for a specific language.
    This only shows the actual translated files, not the placeholders created with
    build-all.
    Takes an optional LANG argument with the name of the language to serve, by default
    en.
    """

    if lng_code is None:
        lng_code = "en"
    lng_path: Path = DOCS_PATH / lng_code
    os.chdir(lng_path)
    serve(dev_addr="127.0.0.1:8009")