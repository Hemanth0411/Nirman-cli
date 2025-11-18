import pytest
from nirman.yaml_parser import parse_yaml_tree


def test_simple_yaml_tree():
    yaml_data = """
project:
  src:
    - main.py
    - utils:
        - helper.py
  tests:
    - test_main.py
  files:
    - README.md
"""

    expected = [
        (0, "project", True),
        (1, "src", True),
        (2, "main.py", False),
        (2, "utils", True),
        (3, "helper.py", False),
        (1, "tests", True),
        (2, "test_main.py", False),
        (1, "README.md", False),
    ]

    parsed = parse_yaml_tree(yaml_data)
    assert parsed == expected

