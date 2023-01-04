# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from pathlib import Path


def copy_existing_docs(src_path: Path, dest_path: Path) -> None:
    with open(dest_path, "w") as dest_file:
        with open(src_path) as src_file:
            dest_file.writelines(src_file.readlines())
    return None


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pyyamlconf"
copyright = "2023, Karthik Rangasai Sivaraman"
author = "Karthik Rangasai Sivaraman"

SOURCE_DIR_ROOT = Path(__file__).resolve().parent.absolute()
DOCS_ROOT = SOURCE_DIR_ROOT.parent
PROJECT_ROOT = DOCS_ROOT.parent

GENERATED_DIR = SOURCE_DIR_ROOT / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

EXISTING_DOCS_NEW_PATHS_MAPPING = {
    file_name: PROJECT_ROOT / file_name for file_name in ["README.md", "CONTRIBUTING.md", "CHANGELOG.md"]
}


for file_name, existing_file_name in EXISTING_DOCS_NEW_PATHS_MAPPING.items():
    copy_existing_docs(existing_file_name, GENERATED_DIR / file_name)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
]

napoleon_google_docstring = True

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
