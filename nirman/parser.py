import re
from typing import List, Tuple

# A set for fast, case-insensitive lookup of Windows reserved names.
# We also include '.' and '..' which are special on all platforms.
RESERVED_NAMES = {
    "con", "prn", "aux", "nul",
    "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
    ".", ".."
}

# Regex for invalid characters, EXCLUDING slashes which are handled separately.
INVALID_CHARS_REGEX = r'[<>:"|?*]'

def parse_markdown_tree(lines: List[str]) -> List[Tuple[int, str, bool]]:
    """
    Parse a markdown tree structure into a list of tuples representing the file/folder hierarchy.
    
    Args:
        lines: A list of strings, where each string is one line from the input Markdown file.
        
    Returns:
        A list of tuples. Each tuple contains:
        - depth (int): The level of the item in the tree
        - name (str): The clean name of the file or folder
        - is_directory (bool): True if it's a directory, False if it's a file
    """
    tree = []
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line.strip():
            continue

        # If a line has --- or ───, skip it with a warning.
        if re.search(r'-{3,}|─{3,}', line):
            print(f"Warning: Skipping malformed line {i + 1}: '{line.strip()}'")
            continue
        # Skip lines with mixed or irregular tree connectors like ──-, -─, --──, etc.
        if re.search(r'(─-)|(-─)|(--─)|(─--)', line):
            print(f"Warning: Skipping malformed connector on line {i + 1}: '{line.strip()}'")
            continue

        # Split the line to isolate the name from the tree symbols.
        parts = re.split(r'--|──', line)
        if len(parts) > 1:
            raw_name = parts[-1].strip()
            # Find the position of the name to determine the prefix.
            prefix_end_index = line.rfind(parts[-2]) + len(parts[-2])
            prefix = line[:prefix_end_index]
        else:
            # This is the root item.
            raw_name = line.strip().split()[0]
            prefix = ""
            is_directory = False

        if not raw_name:
            continue
        clean_name = raw_name.split()[0]

        # Calculate depth based on indentation width
        if not prefix:
            depth = 0
        else:
            depth = (len(prefix) // 4) + 1

        # 1. First, determine if it's a directory from the raw name.
        is_directory = raw_name.endswith(('/', '\\'))

        # 2. Then, create the clean_name by stripping the slashes.
        clean_name = raw_name.strip('\\/')

        # 3. Now, sanitize the clean_name for invalid characters.
        clean_name = re.sub(INVALID_CHARS_REGEX, '_', clean_name)

        # 4. Finally, sanitize for reserved system names.
        base_name = clean_name.split('.')[0]
        if base_name.lower() in RESERVED_NAMES:
            clean_name = "_" + clean_name

        is_directory = raw_name.endswith(('/', '\\'))
        clean_name = raw_name.strip('\\/')

        # Get the base name before any extension for the check.
        base_name = clean_name.split('.')[0]
        if base_name.lower() in RESERVED_NAMES:
            clean_name = "_" + clean_name

        if clean_name == '.' and depth == 0:
            is_directory = True

        tree.append((depth, clean_name, is_directory))

    # --- Post-process to infer directories based on structure ---
    for i in range(len(tree) - 1):
        current_depth, current_name, current_is_dir = tree[i]
        next_depth, _, _ = tree[i + 1]

        # If the next line is visually deeper, current must be a folder
        if not current_is_dir and next_depth > current_depth:
            tree[i] = (current_depth, current_name, True)
    
    return tree
