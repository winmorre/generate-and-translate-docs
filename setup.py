from setuptools import setup, find_packages

setup(
    name="translate_docs",
    version="0.1.0",
    description="...",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "mkdocs",
        "googletrans==3.1.0a0",
    ],
    entry_points={
        "console_scripts": [
            "docs_cli = scripts.cli.docs_cli:cli"
        ]
    },
    author="Jason Joy Atsu Winmorre",
    author_email="jasonjoywinmorre@gmail.com",
)
