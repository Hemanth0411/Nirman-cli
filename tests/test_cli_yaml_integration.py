import sys
from pathlib import Path

def test_cli_yaml_end_to_end(tmp_path, monkeypatch):
    """
    Integration test: create a YAML file, run the CLI, and verify files are created.
    """
    yaml_content = """
project:
  src:
    - main.py
    - utils:
        - helper.py
  files:
    - README.md
"""

    input_file = tmp_path / "structure.yml"
    input_file.write_text(yaml_content, encoding="utf-8")

    output_dir = tmp_path / "out"

    # Monkeypatch argv to simulate CLI call: program_name, input_file, -o, output_dir
    monkeypatch.setattr(sys, "argv", ["nirman", str(input_file), "-o", str(output_dir)])

    # Import and call CLI main
    from nirman import cli
    cli.main()

    # Assertions: ensure structure exists
    assert (output_dir / "project").is_dir()
    assert (output_dir / "project" / "src").is_dir()
    assert (output_dir / "project" / "src" / "main.py").is_file()
    assert (output_dir / "project" / "src" / "utils").is_dir()
    assert (output_dir / "project" / "src" / "utils" / "helper.py").is_file()
    assert (output_dir / "project" / "README.md").is_file()