import json
import logging
from typing import Any
import pathlib

from json_repair import json_repair

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


def load_json(data: str) -> dict | list | None:
    """Load json from string. Return dict if valid, None if not.

    🚨 Tries to fix invalid json using https://github.com/mangiucugna/json_repair lib.
    """
    result = None
    try:
        result = json_repair.loads(data)
    except Exception:  # noqa: Expected from json_repair lib.
        _logger.warning("failed to load json from string!")

        # Try to fix case when keys and values are single quoted.
        # TODO: Naive approach also replaces value/key content if it contains single quotes!
        data = data.replace("'", '"')
        try:
            result = json_repair.loads(data)
        except Exception:
            _logger.warning("failed to load json from string even after replacing ' with \"!")
            pass
    finally:
        return result
