import argparse
import sys
from pathlib import Path

from .parser import parse_markdown_tree
from .builder import build_structure
from .yaml_parser import parse_yaml_tree

def main():
    """The main entry point for the Nirman CLI."""
    parser = argparse.ArgumentParser(
        description="Build a project structure from a Markdown tree file."
    )

    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the Markdown file containing the project structure."
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        type=str,
        help="Target directory where the structure will be created (default: current directory)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actions that would be taken without creating any files or directories."
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite existing files if they are encountered."
    )

    args = parser.parse_args()

    # --- 1. Read the input file ---
    input_path = Path(args.input_file)
    if not input_path.is_file():
        print(f"Error: Input file not found at '{input_path}'")
        sys.exit(1)
    
    valid_extensions = {'.md', '.markdown', '.yaml', '.yml'}
    ext = input_path.suffix.lower()
    if ext not in valid_extensions:
        print(f"Error: Unsupported file type '{ext}'.")
        print("Supported: .md, .markdown, .yml, .yaml")
        sys.exit(1)

    parsed_tree = None
    try:
        if ext in {'.md', '.markdown'}:
            # read lines (existing flow)
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            parsed_tree = parse_markdown_tree(lines)

        elif ext in {'.yml', '.yaml'}:
            # read whole YAML and parse to tree
            with open(input_path, 'r', encoding='utf-8') as f:
                yaml_text = f.read()
            parsed_tree = parse_yaml_tree(yaml_text)
    except Exception as e:
        print(f"Error: Failed to parse input file '{input_path}': {e}")
        sys.exit(1)

    if not parsed_tree:
        print("Warning: Parsed tree is empty. No structure to build.")
        return

    # --- 3. Build the file system ---
    if args.dry_run:
        print("\n--- Starting Dry Run (no changes will be made) ---")
    else:
        print(f"\n--- Building structure in '{Path(args.output).resolve()}' ---")
    
    build_structure(
        tree=parsed_tree,
        output_path=args.output,
        dry_run=args.dry_run,
        force=args.force
    )
    
    print("\nNirman has finished.")