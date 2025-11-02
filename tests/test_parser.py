# tests/test_parser.py

import pytest
from nirman.parser import parse_markdown_tree

# A standard Markdown tree for testing
MARKDOWN_INPUT = [
    "project-root/",
    "├── src/",
    "│   ├── main.py",
    "│   └── utils/",
    "│       └── helper.py",
    "├── tests/",
    "│   └── test_main.py",
    "└── README.md",
]

# The expected output from the parser
EXPECTED_OUTPUT = [
    (0, "project-root", True),
    (1, "src", True),
    (2, "main.py", False),
    (2, "utils", True),
    (3, "helper.py", False),
    (1, "tests", True),
    (2, "test_main.py", False),
    (1, "README.md", False),
]

def test_parse_standard_markdown_tree():
    """
    Tests that the parser correctly converts a standard Markdown tree.
    """
    parsed_tree = parse_markdown_tree(MARKDOWN_INPUT)
    assert parsed_tree == EXPECTED_OUTPUT

def test_parser_with_empty_lines():
    """
    Tests that the parser handles empty lines gracefully.
    """
    input_with_empty_lines = [
        "project/",
        "",
        "├── file.txt",
        "",
    ]
    expected = [
        (0, "project", True),
        (1, "file.txt", False),
    ]
    parsed_tree = parse_markdown_tree(input_with_empty_lines)
    assert parsed_tree == expected

def test_parser_root_is_dot():
    """
    Tests parsing when the root of the structure is '.'
    """
    input_data = [
        ".",
        "|-- main.py",
        "|-- app/",
        "|   |-- __init__.py"
    ]
    expected = [
        (0, ".", True),
        (1, "main.py", False),
        (1, "app", True),
        (2, "__init__.py", False)
    ]
    assert parse_markdown_tree(input_data) == expected

def test_parser_alternative_syntax():
    """
    Tests parsing with alternative tree symbols ('|--') and dir separators ('\').
    """
    input_data = [
        "app\\",
        "|-- main.py",
        "|-- services\\",
        "|   |-- user_service.py"
    ]
    expected = [
        (0, "app", True),
        (1, "main.py", False),
        (1, "services", True),
        (2, "user_service.py", False)
    ]
    assert parse_markdown_tree(input_data) == expected