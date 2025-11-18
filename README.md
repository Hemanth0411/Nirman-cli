# Nirman-cli

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/pypi/v/Nirman-cli?color=blue&label=pypi%20package" alt="PyPI Version">
  </a>
  <a href="https://github.com/Hemanth0411/Nirman-cli/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Hemanth0411/Nirman-cli" alt="License">
  </a>
</p>

A simple and powerful CLI tool to create project folder and file structures from **Markdown** and **YAML** tree definitions.

Stop creating files and folders manually. Define your project’s skeleton in a readable Markdown or YAML file, and let `nirman` build it for you in seconds.

## Key Features

* **Two Input Formats:**

  * Markdown (`.md`, `.markdown`)
  * YAML (`.yml`, `.yaml`)
* **Readable Tree Syntax:** Write clean collapsible structures.
* **Safe Execution:** Preview actions with `--dry-run`.
* **Flexible:** Overwrite files using `--force`.
* **Lightweight & Fast:** Uses simple tree-based parsing.
* **Cross-platform:** Works on Linux, macOS, and Windows.

---

## Installation

Install from PyPI:

```bash
pip install Nirman-cli
```

---

# Usage

## 1) Markdown Example

Create a file `structure.md`:

```markdown
my-python-app/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
└── README.md
```

Build the structure:

```bash
nirman structure.md
```

---

## 2) YAML Example

Nirman also supports YAML.
**Rule:** Individual files must be listed under a `files:` key.

Example (`structure.yml`):

```yaml
project:
  src:
    files:
      - main.py
      - utils.py
  services:
    api:
      files:
        - handler.py
        - routes.py
  files:
    - README.md
    - .gitignore
```

Build it:

```bash
nirman structure.yml
```

This produces:

```
output_folder/
└── project/
    ├── src/
    │   ├── main.py
    │   └── utils.py
    ├── services/
    │   └── api/
    │       ├── handler.py
    │       └── routes.py
    ├── README.md
    └── .gitignore
```

---

# Command-Line Options

```
usage: nirman [-h] [-o OUTPUT] [--dry-run] [-f] input_file

Build a project structure from a Markdown (.md) or YAML (.yml/.yaml) file.

positional arguments:
  input_file            Path to the structure file.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Target directory where the structure will be created (default: current directory).
  --dry-run             Print the actions that would be taken without creating any files or directories.
  -f, --force           Overwrite existing files if they are encountered.
```

---

# YAML Rules (Important)

Your YAML structure must follow these rules:

1. **Every folder is a dictionary key.**
2. **All direct files inside a folder must be placed under:**

   ```yaml
   files:
     - file1.txt
     - file2.py
   ```
3. Nested folders must be dictionaries.
4. Lists may contain:

   * file names (strings)
   * dictionaries for nested folders

This rule is reflected in the updated parser:

```python
# Individual files must be under "files:"
if key == "files":
    ...
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Hemanth0411/Nirman-cli/blob/main/LICENSE) file for details.
