# **Nirman-cli**

A clean, fast CLI tool to generate project folder structures from **Markdown** or **YAML** definitions.
Stop clicking around in file explorers — describe your structure once, build it instantly.

---

## **✨ Features**

* **Two input formats**

  * Markdown (`.md`, `.markdown`)
  * YAML (`.yml`, `.yaml`)
* **Tree-based, human-readable syntax**
* **Dry-run mode** to preview without writing
* **Force overwrite** for regenerating projects
* **Cross-platform** (Linux, macOS, Windows)
* Zero learning curve — simple, predictable behavior

---

## **📦 Installation**

```bash
pip install Nirman-cli
```

---

## **🚀 Quick Start**

### **1) Markdown**

**structure.md**

```
my-python-app/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
└── README.md
```

Generate:

```bash
nirman structure.md
```

Creates the project inside the **current directory**.
(Use `-o` to output elsewhere.)

---

### **2) YAML**

YAML uses a clean folder → files pattern.
**Files MUST be under a `files:` key.**

**structure.yml**

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

Generate:

```bash
nirman structure.yml
```

---

## **📂 Output Structure Example**

```
project/
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

## **🛠 CLI Reference**

```
nirman [-h] [-o OUTPUT] [--dry-run] [-f] input_file
```

### **Arguments**

| Argument     | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| `input_file` | Markdown (.md/.markdown) or YAML (.yml/.yaml) structure file |

### **Options**

| Option         | Description                                   |
| -------------- | --------------------------------------------- |
| `-o, --output` | Target directory (default: current directory) |
| `--dry-run`    | Show actions without creating anything        |
| `-f, --force`  | Overwrite existing files                      |

---

## **📘 YAML Rules (Important)**

You must follow these rules when writing YAML structures:

1. **Every folder is a dict key**

2. **Files go under the `files:` key**

   ```yaml
   files:
     - file1.py
     - file2.txt
     - config.json
   ```

3. Nested folders must be dictionaries

4. Lists can contain:

   * filenames (strings)
   * folders (dictionary items)

This enforces a clean, consistent YAML tree.

---

## **🧪 Running Tests (For Contributors)**

```bash
pytest
```

Includes:

* Parser tests
* CLI integration tests
* YAML rule enforcement tests

---

## **🔧 Local Development Setup**

```bash
git clone https://github.com/Hemanth0411/Nirman-cli
cd Nirman-cli
pip install -e .
```

Run CLI from source:

```bash
nirman example.yml
```

---

## **📄 License**

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Hemanth0411/Nirman-cli/blob/main/LICENSE) file for details.
