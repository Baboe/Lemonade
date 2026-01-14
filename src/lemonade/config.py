"""Configuration and paths for Lemonade."""

from pathlib import Path

# Canonical queue root - DO NOT CHANGE
# Tools are disposable, the queue location is stable.
QUEUE_ROOT = Path(r"C:\tresor\etsy\queue")

# Queue folder names
INBOX = "INBOX"
READY = "READY"
TODAY = "TODAY"
DRAFTED = "DRAFTED"
PUBLISHED = "PUBLISHED"

# All queue folders in order
QUEUE_FOLDERS = [INBOX, READY, TODAY, DRAFTED, PUBLISHED]


def get_queue_path(folder: str) -> Path:
    """Get the full path to a queue folder."""
    if folder not in QUEUE_FOLDERS:
        raise ValueError(f"Invalid queue folder: {folder}. Must be one of {QUEUE_FOLDERS}")
    return QUEUE_ROOT / folder


def ensure_queue_folders_exist() -> dict[str, Path]:
    """
    Ensure all queue folders exist, creating them if necessary.
    
    Returns:
        Dictionary mapping folder names to their paths.
    
    Raises:
        OSError: If folders cannot be created.
    """
    paths = {}
    for folder in QUEUE_FOLDERS:
        path = QUEUE_ROOT / folder
        path.mkdir(parents=True, exist_ok=True)
        paths[folder] = path
    return paths


def count_product_folders(folder: str) -> int:
    """
    Count the number of product folders in a queue folder.
    
    A product folder is any subdirectory (not files) in the queue folder.
    
    Args:
        folder: Queue folder name (INBOX, READY, etc.)
    
    Returns:
        Number of product folders.
    
    Raises:
        FileNotFoundError: If the queue folder does not exist.
    """
    path = get_queue_path(folder)
    if not path.exists():
        raise FileNotFoundError(f"Queue folder does not exist: {path}")
    
    return sum(1 for item in path.iterdir() if item.is_dir())
