import sys
import os


def include_root():
    # Navigate two levels up to ensure we reach the project root
    notebook_dir = os.getcwd()
    project_root = os.path.abspath(os.path.join(notebook_dir, ".."))  # Adjust if needed

    # Verify the path is correct
    print(f"Project root: {project_root}")
    print(f"Notebook directory: {notebook_dir}")

    # Add project root to sys.path
    if project_root not in sys.path:
        sys.path.append(project_root)

    # Verify Python paths
    print("sys.path:", sys.path)
