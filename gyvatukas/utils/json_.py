import json
import logging
from typing import Any
import pathlib

from gyvatukas.utils.fs import read_file, write_file

_logger = logging.getLogger("gyvatukas")


def get_pretty_json(data: dict | list) -> str:
    """Return pretty json string."""
    result = json.dumps(data, indent=4, default=str, ensure_ascii=False)
    return result


def read_json(path: pathlib.Path, default: Any = None) -> dict | list:
    """Read json from file. Return empty dict if not found or invalid json."""
    data = read_file(path=path)
    if data:
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            pass
    if default is not None:
        return default
    return {}


def write_json(
    path: pathlib.Path, data: dict | list, pretty: bool = True, override: bool = False
) -> bool:
    """Write json to file. Return true if written, false if not."""
    if pretty:
        content = get_pretty_json(data)
    else:
        content = json.dumps(data, default=str, ensure_ascii=False)

    result = write_file(path=path, content=content, override=override)
    return result
