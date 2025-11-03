import argparse
import sys
from pathlib import Path

from .parser import parse_markdown_tree
from .builder import build_structure

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
    
    valid_extensions = {'.md', '.markdown'}
    if input_path.suffix.lower() not in valid_extensions:
        print(
            f"\nNote: The file '{input_path.name}' doesn't seem to be a Markdown file.\n"
            "Nirman currently supports only Markdown files (.md or .markdown) for building structures.\n"
            "Please provide a valid Markdown file and try again."
        )
        sys.exit(0)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error: Could not read the input file: {e}")
        sys.exit(1)
        
    # --- 2. Parse the structure ---
    print("Parsing structure...")
    parsed_tree = parse_markdown_tree(lines)
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