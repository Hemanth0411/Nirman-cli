import pytest
from pathlib import Path
from nirman.builder import build_structure

# A sample parsed tree, like the output from your parser
SAMPLE_TREE = [
    (0, "project-root", True),
    (1, "src", True),
    (2, "main.py", False),
    (1, "README.md", False),
]

def test_builder_creates_structure(tmp_path: Path):
    """
    Tests that the builder correctly creates folders and files.
    """
    build_structure(SAMPLE_TREE, output_path=str(tmp_path))

    # Check that all paths were created correctly
    assert (tmp_path / "project-root").is_dir()
    assert (tmp_path / "project-root" / "src").is_dir()
    assert (tmp_path / "project-root" / "src" / "main.py").is_file()
    assert (tmp_path / "project-root" / "README.md").is_file()

def test_builder_dry_run(tmp_path: Path):
    """
    Tests that dry_run prints actions but creates no files or folders.
    """
    build_structure(SAMPLE_TREE, output_path=str(tmp_path), dry_run=True)

    # Check that nothing was created
    # `iterdir()` returns a generator, we check if it's empty.
    assert not any(tmp_path.iterdir())

def test_builder_force_overwrite(tmp_path: Path):
    """
    Tests that the `force` flag correctly overwrites existing files.
    """
    # Create a pre-existing file with content
    project_dir = tmp_path / "project-root"
    project_dir.mkdir()
    readme_file = project_dir / "README.md"
    readme_file.write_text("Original content")

    # Run build WITHOUT force - content should remain
    build_structure(SAMPLE_TREE, output_path=str(tmp_path), force=False)
    assert readme_file.read_text() == "Original content"

    # Run build WITH force - content should be gone (file is truncated by touch())
    build_structure(SAMPLE_TREE, output_path=str(tmp_path), force=True)
    assert readme_file.read_text() == ""

def test_builder_handles_dot_root(tmp_path: Path):
    """
    Tests that the builder works correctly when the parsed tree's root is '.'
    """
    tree_with_dot = [
        (0, ".", True),
        (1, "main.py", False),
        (1, "app", True),
    ]
    build_structure(tree_with_dot, output_path=str(tmp_path))
    
    # The structure should be created directly inside tmp_path, not a '.' folder
    assert (tmp_path / "main.py").is_file()
    assert (tmp_path / "app").is_dir()
    # Ensure no literal entry named '.' was created inside tmp_path
    assert "." not in [p.name for p in tmp_path.iterdir()]