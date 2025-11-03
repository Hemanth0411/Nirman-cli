import re
from typing import List, Tuple

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
    
    for line in lines:
        line = line.rstrip()
        if not line.strip():
            continue

        # Split the line to isolate the name from the tree symbols.
        parts = re.split(r'--|──', line)
        if len(parts) > 1:
            name = parts[-1].strip()
            # Find the position of the name to determine the prefix.
            prefix_end_index = line.rfind(parts[-2]) + len(parts[-2])
            prefix = line[:prefix_end_index]
        else:
            # This is the root item.
            name = line.strip()
            prefix = ""

        # Calculate depth based on indentation width
        if not prefix:
            depth = 0
        else:
            depth = (len(prefix) // 4) + 1
        
        is_directory = name.endswith(('/', '\\'))
        clean_name = name.rstrip('\\/')

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
