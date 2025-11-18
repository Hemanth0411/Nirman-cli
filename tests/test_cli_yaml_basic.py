import sys
from pathlib import Path


def test_cli_yaml_basic_generation(tmp_path, monkeypatch):
    yaml_data = """
project:
  files:
    - a.py
    - b.txt
"""

    input_file = tmp_path / "structure.yml"
    input_file.write_text(yaml_data)

    output_dir = tmp_path / "out"

    monkeypatch.setattr(
        sys, "argv",
        ["nirman", str(input_file), "-o", str(output_dir)]
    )

    from nirman.cli import main
    main()

    assert (output_dir / "project").is_dir()
    assert (output_dir / "project" / "a.py").is_file()
    assert (output_dir / "project" / "b.txt").is_file()
