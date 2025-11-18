import pytest
from nirman.yaml_parser import parse_yaml_tree


def test_yaml_simple_files_under_files_key():
    yaml_data = """
app:
  files:
    - a.py
    - b.txt
"""
    expected = [
        (0, "app", True),
        (1, "a.py", False),
        (1, "b.txt", False),
    ]

    assert parse_yaml_tree(yaml_data) == expected


def test_yaml_nested_structure_with_files():
    yaml_data = """
project:
  src:
    files:
      - main.py
      - config.json
  utils:
    helpers:
      files:
        - helper.py
"""
    expected = [
        (0, "project", True),
        (1, "src", True),
        (2, "main.py", False),
        (2, "config.json", False),
        (1, "utils", True),
        (2, "helpers", True),
        (3, "helper.py", False),
    ]

    assert parse_yaml_tree(yaml_data) == expected


def test_yaml_dict_without_files_is_folder():
    yaml_data = """
root:
  empty_folder: {}
"""
    expected = [
        (0, "root", True),
        (1, "empty_folder", True),
    ]
    assert parse_yaml_tree(yaml_data) == expected


def test_yaml_list_of_mixed_items():
    yaml_data = """
root:
  items:
    - folder1:
        files:
          - a.py
    - folder2:
        files:
          - b.py
"""
    expected = [
        (0, "root", True),
        (1, "items", True),
        (2, "folder1", True),
        (3, "a.py", False),
        (2, "folder2", True),
        (3, "b.py", False),
    ]

    assert parse_yaml_tree(yaml_data) == expected
