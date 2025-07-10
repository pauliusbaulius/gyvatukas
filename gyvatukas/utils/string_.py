def str_remove_except(s: str, allowed: list[str]) -> str:
    """Remove all characters from `s` except those in `allowed`."""
    return "".join(filter(lambda x: x in allowed, s))


def str_keep_except(s: str, allowed: list[str]) -> str:
    """Keep all characters from `s` except those in `allowed`."""
    return "".join(filter(lambda x: x not in allowed, s))


def human_readable_size(size: int, decimal_places: int = 2) -> str:
    """Convert a size in bytes to a human-readable string.

    Args:
        size: Size in bytes
        decimal_places: Number of decimal places to show (default: 2)

    Returns:
        Formatted string like "1.5 MiB" or "2.00 GiB"
    """
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"
