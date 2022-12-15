import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Pool

from docs import *

cli = typer.Typer()


@cli.command()
def new_lng(lng_code: str = typer.Argument(..., callback=lang_callback)):
    """
    Generate a new docs translation directory for the language LANG.
    LANG should be a 2 or 5 letter language code, like: en, es, de, pt, pt_BR, etc.
    """
    new_path: Path = Path("docs") / lng_code
    # don't generate docs for a language if it already exist
    if new_path.exists():
        typer.echo(f"The language was already created: {lng_code}")
        raise typer.Abort()
    new_path.mkdir()
    new_config = get_base_lng_config(lng_code)
    new_config_path: Path = Path(new_path) / MKDOCS_NAME

    # translate the site description
    new_config["site_description"] = translation(text=new_config["site_description"], dest_lng=lng_code)

    new_config_path.write_text(
        yaml.dump(new_config, sort_keys=False, width=200, allow_unicode=True),
        encoding="utf-8",
    )

    new_config_docs_path: Path = new_path / "docs"
    new_config_docs_path.mkdir()

    file_names = get_all_md_filenames()
    create_new_files(filenames=file_names, new_config_docs_path=new_config_docs_path, lng_code=lng_code)

    # copy all other items to the new generated docs location
    shutil.copytree(DEFAULT_DOCS_PATH / "docs" / "img", new_config_docs_path / "img")
    new_overrides_gitignore_path = new_path / "overrides" / ".gitignore"
    new_overrides_gitignore_path.parent.mkdir(parents=True, exist_ok=True)
    new_overrides_gitignore_path.write_text("")

    typer.secho(f"Successfully initialized: {new_path}", color=typer.colors.GREEN)
    # update the languages section
    update_languages(lang=None)
    # translate the nav section
    translate_navs(lng_code=lng_code)


@cli.command()
def build_lng(
        lng_code: str = typer.Argument(
            ..., callback=lang_callback, autocompletion=complete_existing_lang
        )
):
    """
    Build the docs for a language, filling missing pages with translation notifications.
    """
    build_lng_path, dist_path, lng_path = build_paths(lng_code=lng_code)

    remove_and_copytree(build_lng_path, lng_path)

    nav, lng_config = load_lng_nav_and_en_nav(lng_path=lng_path)

    lng_nav = lng_config["nav"]

    file_to_nav = get_file_to_navigate_to_as_map(nav[2:])

    use_lng_file_to_nav = update_use_lng_file_to_nav(
        language_nav=lng_nav,
        file_to_nav=file_to_nav,
        build_lng_path=build_lng_path)

    key_to_section = generate_key_to_section(file_to_nav=file_to_nav, use_lng_file_to_nav=use_lng_file_to_nav)

    new_nav = update_new_lng_nav(key_to_section=key_to_section)

    save_new_lng_nav(lng_config=lng_config, lng_nav=lng_nav, nav=nav, new_nav=new_nav,
                     build_lng_path=build_lng_path)

    current_dir = os.getcwd()
    os.chdir(build_lng_path)
    subprocess.run(["mkdocs", "build", "--site-dir", dist_path, "--clean"], check=True)
    os.chdir(current_dir)
    typer.secho(f"Successfully built docs for: {lng_code}", color=typer.colors.GREEN)


@cli.command()
def build_all():
    """
    Build mkdocs site for en, and then build each language inside, end result is located
    at directory ./site/ with each language inside.
    """
    site_path = Path("site").absolute()
    update_languages(lang=None)
    current_dir = os.getcwd()
    os.chdir(DEFAULT_DOCS_PATH)
    typer.echo("Building docs for: en")
    subprocess.run(["mkdocs", "build", "--site-dir", site_path], check=True)
    os.chdir(current_dir)
    lngs = []
    for lng in get_lang_paths():
        if lng == DEFAULT_DOCS_PATH or not lng.is_dir():
            continue
        lngs.append(lng.name)
    cpu_count = os.cpu_count() or 1
    with Pool(cpu_count * 2) as p:
        p.map(build_lng, lngs)


@cli.command()
def update_languages(
        lang=typer.Argument(
            None, callback=lang_callback, autocompletion=complete_existing_lang
        )
):
    """
    Update the mkdocs.yml file Languages section including all the available languages.
    The LANG argument is a 2-letter language code. If it's not provided, update all the
    mkdocs.yml files (for all the languages).
    """
    if lang is None:
        typer.echo(f"Lang Paths {get_lang_paths()}")
        for lang_path in get_lang_paths():
            typer.echo(f"Lang pah Name ::  {lang_path.name}")
            if lang_path.is_dir():
                update_single_lng(lang_path.name)
    else:
        update_single_lng(lang)


@cli.command()
def serve():
    """
    A quick server to preview a built site with translations.
    For development, prefer the command live (or just mkdocs serve).
    This is here only to preview a site with translations already built.
    Make sure you run the build-all command first.
    """
    typer.echo("Warning: this is a very simple server.")
    typer.echo("For development, use the command live instead.")
    typer.echo("This is here only to preview a site with translations already built.")
    typer.echo("Make sure you run the build-all command first.")
    os.chdir("site")
    server_address = ("", 8009)
    server = HTTPServer(server_address, SimpleHTTPRequestHandler)
    typer.echo(f"Serving at: http://127.0.0.1:8009")
    server.serve_forever()


@cli.command()
def live(
        lng_code: str = typer.Argument(
            None, callback=lang_callback, autocompletion=complete_existing_lang
        )
):
    """
    Serve with livereload a docs site for a specific language.
    This only shows the actual translated files, not the placeholders created with
    build-all.
    Takes an optional LANG argument with the name of the language to serve, by default
    en.
    """
    if lng_code is None:
        lng_code = "en"
    lang_path: Path = DOCS_PATH / lng_code
    os.chdir(lang_path)
    mkdocs.commands.serve.serve(dev_addr="127.0.0.1:8009")


if __name__ == "__main__":
    cli()
