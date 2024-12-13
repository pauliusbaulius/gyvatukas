def str_remove_except(s: str, allowed: list[str]) -> str:
    """Remove all characters from `s` except those in `allowed`."""
    return "".join(filter(lambda x: x in allowed, s))


def str_keep_except(s: str, allowed: list[str]) -> str:
    """Keep all characters from `s` except those in `allowed`."""
    return "".join(filter(lambda x: x not in allowed, s))
