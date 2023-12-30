# TODO: get_by_path(d, path: str) -> d[a][b][c] as path=a.b.c


def dict_remove_matching_values(d: dict, values: list) -> dict:
    """Remove all key-value pairs from dict where value is in values.
    Useful for removing None values from dict or empty strings when working with form data.

    Returns new dict.
    🐌 Creates a new dict, not recommended for large dicts.
    """
    # TODO: Recursive iteration to remove deeply matched values? But as a separate function.
    new_d = {}
    for k, v in d.items():
        if v not in values:
            new_d[k] = v

    return new_d
