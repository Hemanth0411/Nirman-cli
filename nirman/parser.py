import re
from typing import List, Tuple

def sanitize_filename(name: str) -> str:
    """
    Removes illegal characters from a filename and handles reserved names
    to make it safe for the filesystem (especially Windows).
    """
    # 1. Remove illegal characters: < > : " / \ | ? *
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name)
    
    # 2. Handle Windows reserved names (case-insensitive)
    reserved_names = {
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2",
        "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    
    # Check if the name (without extension) is a reserved name
    name_part = sanitized_name.split('.')[0]
    if name_part.upper() in reserved_names:
        sanitized_name = f"_{sanitized_name}"

    # 3. Remove leading/trailing spaces and dots, which are also problematic
    sanitized_name = sanitized_name.strip(' .')

    # 4. If the name becomes empty after sanitization, provide a default
    if not sanitized_name:
        return "_renamed_"
        
    return sanitized_name


def parse_markdown_tree(lines: List[str]) -> List[Tuple[int, str, bool]]:
    """
    Parse a markdown tree structure into a list of tuples representing the file/folder hierarchy.
    """
    tree = []
    tree_line_regex = re.compile(r"^(?P<prefix>[\s│]*[└├]──?)?\s*(?P<name>.+)")

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

        branch_pos = -1
        if '├' in prefix: branch_pos = prefix.find('├')
        elif '└' in prefix: branch_pos = prefix.find('└')
        depth = (branch_pos // 4) + 1 if branch_pos != -1 else 0
        
        # Check for directory status BEFORE sanitizing, as slashes will be removed
        is_directory = name.endswith(('/', '\\'))
        
        # --- THIS IS THE KEY CHANGE ---
        # Sanitize the name to make it safe for the filesystem
        clean_name = name.strip('\\/')
        sanitized_name = sanitize_filename(clean_name)

        if sanitized_name == '.' and depth == 0:
            is_directory = True

        tree.append((depth, sanitized_name, is_directory))

    # Post-process to infer directories based on structure
    for i in range(len(tree) - 1):
        current_depth, current_name, current_is_dir = tree[i]
        next_depth, _, _ = tree[i + 1]
        if not current_is_dir and next_depth > current_depth:
            tree[i] = (current_depth, current_name, True)
    
    return tree
