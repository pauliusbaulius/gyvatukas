def remove_except(s: str, allowed: list[str]) -> str:
    """Remove all characters from `s` except those in `allowed`."""
    return "".join(filter(lambda x: x in allowed, s))


def keep_except(s: str, allowed: list[str]) -> str:
    """Keep all characters from `s` except those in `allowed`."""
    return "".join(filter(lambda x: x not in allowed, s))
