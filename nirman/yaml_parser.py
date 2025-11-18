import yaml
from typing import Any, List, Tuple


def parse_yaml_tree(yaml_text: str) -> List[Tuple[int, str, bool]]:
    data = yaml.safe_load(yaml_text)
    tree: List[Tuple[int, str, bool]] = []

    def walk(node: Any, depth: int):
        if isinstance(node, dict):
            for key, value in node.items():

                # --- SPECIAL CASE: handle `files` as direct files ---
                if key == "files":
                    if isinstance(value, list):
                        for item in value:
                            tree.append((depth, str(item), False))
                    else:
                        tree.append((depth, str(value), False))
                    continue

                # Normal dict key = folder
                tree.append((depth, key, True))
                walk(value, depth + 1)

        elif isinstance(node, list):
            for item in node:
                if isinstance(item, dict):
                    for key, value in item.items():
                        tree.append((depth, key, True))
                        walk(value, depth + 1)
                else:
                    tree.append((depth, str(item), False))

        else:
            tree.append((depth, str(node), False))

    walk(data, 0)
    return tree
