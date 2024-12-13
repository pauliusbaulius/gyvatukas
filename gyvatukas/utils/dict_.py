from typing import Any

from gyvatukas.exceptions import GyvatukasException


def dict_remove_matching_values(d: dict, values: list) -> dict:
    """Remove all key-value pairs from dict where value is in values.
    Useful for removing None values from dict or empty strings when working with form data.

    Returns new dict.
    🐌 Creates a new dict, not recommended for large dicts.
    """
    new_d = {}
    for k, v in d.items():
        if v not in values:
            new_d[k] = v

    return new_d


def dict_get_by_path(
    d: dict, path: str, separator: str = ".", allow_none: bool = False
) -> Any:
    current = d

    if not path:
        return current

    for part in path.split(separator):
        try:
            if isinstance(current, (list, tuple)):
                try:
                    index = int(part)
                    current = current[index]
                except (ValueError, IndexError):
                    if allow_none:
                        return None
                    raise GyvatukasException(f"invalid index '{part}' for sequence")
            elif isinstance(current, dict):
                current = current[part]
            else:
                if allow_none:
                    return None
                raise GyvatukasException(
                    f"cannot index into {type(current)} with '{part}'"
                )
        except KeyError:
            if allow_none:
                return None
            raise

    return current
