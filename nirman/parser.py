import re
from typing import List, Tuple

def sanitize_filename(name: str) -> str:
    """
    Removes illegal characters from a filename and handles reserved names
    to make it safe for the filesystem (especially Windows).
    """
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name)
    
    reserved_names = {
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2",
        "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    
    name_part = sanitized_name.split('.')[0]
    if name_part.upper() in reserved_names:
        sanitized_name = f"_{sanitized_name}"

    sanitized_name = sanitized_name.strip(' .')

    if not sanitized_name:
        return "_renamed_"
        
    return sanitized_name


def parse_markdown_tree(lines: List[str]) -> List[Tuple[int, str, bool]]:
    """
    Parse a markdown tree structure into a list of tuples representing the file/folder hierarchy.
    """
    tree = []
    
    # --- FIX #1: Make the regex more flexible to accept ASCII trees like '|--' ---
    # It now accepts │, |, or whitespace for indentation, and ├, └, |, or + for branches.
    tree_line_regex = re.compile(r"^(?P<prefix>[\s│|]*([└├|+]-{2})?)?\s*(?P<name>.+)")

    for line in lines:
        line = line.rstrip()
        if not line.strip():
            continue

        match = tree_line_regex.match(line)
        if not match:
            print(f"Warning: Skipping malformed or non-tree line: '{line}'")
            continue

        parts = match.groupdict()
        prefix = parts.get("prefix") or ""
        name = parts.get("name", "").strip()

        if not name:
            continue
            
        # This part of the prefix is the visual tree structure (e.g., "|-- " or "├── ")
        branch_part = parts.group(2) or ''

        # Depth is now calculated based on the position of the branch part
        if branch_part:
            depth = (line.find(branch_part) // 4) + 1
        else:
            depth = 0
        
        is_directory = name.endswith(('/', '\\'))
        clean_name = name.strip('\\/')

        # --- FIX #2: Add a special case for the '.' root to prevent sanitization ---
        if clean_name == '.' and depth == 0:
            sanitized_name = '.'
            is_directory = True
        else:
            sanitized_name = sanitize_filename(clean_name)

        tree.append((depth, sanitized_name, is_directory))

    # Post-process to infer directories based on structure
    for i in range(len(tree) - 1):
        current_depth, current_name, current_is_dir = tree[i]
        next_depth, _, _ = tree[i + 1]
        if not current_is_dir and next_depth > current_depth:
            tree[i] = (current_depth, current_name, True)
    
    return tree
