from setuptools import setup, find_packages

setup(
    name="scripts",
    version="0.1.0",
    description="...",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "mkdocs",
        "googletrans==3.1.0a0",
        "mkdocs-material",
        "mkdocs-material-extensions"
    ],
    entry_points={
        "console_scripts": [
            "cli=scripts.cli:cli"
        ]
    },
    author="Jason Joy Atsu Winmorre",
    author_email="jasonjoywinmorre@gmail.com",
)
