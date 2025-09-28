import os

def is_directory_empty(path):
    """
    Checks if a directory is empty using os.scandir().
    Returns True if the directory is empty, False otherwise.
    """
    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path}' is not a valid directory.")
    with os.scandir(path) as it:
        return not any(it)
