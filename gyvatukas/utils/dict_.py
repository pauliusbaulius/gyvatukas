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


def dict_flatten(d: dict, parent_key: str = "", separator: str = ".") -> dict:
    if not isinstance(d, dict):
        raise TypeError("Input must be a dictionary")

    items = []

    for key, value in d.items():
        try:
            str_key = str(key)
        except Exception:
            raise TypeError(f"Dictionary key {key!r} cannot be converted to string")

        if separator in str_key:
            raise ValueError(
                f"Dictionary key '{str_key}' cannot contain separator '{separator}'"
            )

        new_key = f"{parent_key}{separator}{str_key}" if parent_key else str_key

        if isinstance(value, dict):
            items.extend(dict_flatten(value, new_key, separator).items())
        elif isinstance(value, (list, tuple)):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    items.extend(
                        dict_flatten(
                            item, f"{new_key}{separator}{i}", separator
                        ).items()
                    )
                else:
                    items.append((f"{new_key}{separator}{i}", item))
        else:
            items.append((new_key, value))

    return dict(items)


if __name__ == "__main__":
    d = {"a": {"b": {"c": 123}}, "foo.bar": [1, 2, "something"]}
    print(dict_flatten(d, separator=">"))
