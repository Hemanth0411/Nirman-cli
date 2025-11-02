# Nirman-cli

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/pypi/v/Nirman-cli?color=blue&label=pypi%20package" alt="PyPI Version">
  </a>
  <a href="https://github.com/Hemanth0411/Nirman-cli/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Hemanth0411/Nirman-cli" alt="License">
  </a>
</p>

A simple and powerful CLI tool to create project folder and file structures from a Markdown tree.

Stop creating files and folders manually. Define your project's skeleton in a readable Markdown file and let `nirman` build it for you in seconds.

## Key Features

-   **Intuitive Input:** Uses a visual, tree-style Markdown format.
-   **Safe by Default:** Includes a `--dry-run` mode to preview changes.
-   **Flexible:** Supports overwriting files with the `--force` flag.
-   **Simple & Lightweight:** No external dependencies.

## Installation

You can install `Nirman-cli` directly from PyPI:

```bash
pip install Nirman-cli
```

## Usage

1.  Create a Markdown file (e.g., `structure.md`) defining your desired project layout:

    ```markdown
    my-python-app/
    ├── src/
    │   ├── __init__.py
    │   └── main.py
    ├── tests/
    │   └── test_main.py
    ├── .gitignore
    └── README.md
    ```

2.  Run the `nirman` command from your terminal:

    ```bash
    nirman structure.md
    ```

    This will create the `my-python-app/` directory and all its contents in your current location.

### Command-Line Options

```
usage: nirman [-h] [-o OUTPUT] [--dry-run] [-f] input_file

Build a project structure from a Markdown tree file.

positional arguments:
  input_file            Path to the Markdown file containing the project structure.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Target directory where the structure will be created (default: current directory).
  --dry-run             Print the actions that would be taken without creating any files or directories.
  -f, --force           Overwrite existing files if they are encountered.
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Hemanth0411/Nirman-cli/blob/main/LICENSE) file for details.
