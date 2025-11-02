from pathlib import Path
from typing import List, Tuple


def build_structure(
    tree: List[Tuple[int, str, bool]],
    output_path: str,
    dry_run: bool = False,
    force: bool = False
):
    """
    Build a file/folder structure on disk from a parsed tree representation.
    
    Args:
        tree: List of tuples (depth, name, is_directory) from parse_markdown_tree
        output_path: The directory where the structure should be created
        dry_run: If True, print actions without making changes
        force: If True, overwrite existing files
    """
    # 1. Initialization
    # Check if tree is empty
    if not tree:
        print("Empty tree provided. Nothing to create.")
        return
    
    # Convert output_path to Path object
    root_path = Path(output_path)
    
    # Initialize path stack with the root
    path_stack = [root_path]
    
    # 2. Handle '.' root (Special Case)
    has_dot_root = False
    if tree and tree[0][1] == '.':
        has_dot_root = True
        tree = tree[1:]  # Remove the dot root
        # Adjust depths of remaining items
        tree = [(depth - 1, name, is_dir) for depth, name, is_dir in tree]
    
    # 3. Iterate Through the Tree
    for depth, name, is_directory in tree:
        # Skip literal '.' entries (don't create a './.' under output_path)
        if name == '.':
            continue
        # Normalize negative depths and make parent selection defensive
        depth = max(0, depth)
        
        # Reset path_stack to appropriate depth
        path_stack = path_stack[: depth + 1]
        # If depth exceeds current stack, use the last entry as parent
        parent_index = depth if depth < len(path_stack) else (len(path_stack) - 1)
        parent_path = path_stack[parent_index]
        
        # Calculate the current path
        current_path = parent_path / name
        
        # 4. Process Directories
        if is_directory:
            print(f"Creating DIR: {current_path}")
            
            if not dry_run:
                current_path.mkdir(parents=True, exist_ok=True)
            
            # Add the current directory to the stack
            path_stack.append(current_path)
        
        # 5. Process Files
        else:
            # Print action; only modify filesystem when not a dry run
            print(f"Creating FILE: {current_path}")
            
            if not dry_run:
                # Ensure parent directory exists before creating the file
                current_path.parent.mkdir(parents=True, exist_ok=True)
                # Create or overwrite the file
                if not current_path.exists() or force:
                    current_path.write_text("")  # Replace touch() with write_text("")
                    assert current_path.is_file()  # Verify file creation
