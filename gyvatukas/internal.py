import importlib.metadata
import pathlib

import appdirs


def get_gyvatukas_version() -> str:
    """Returns the version of the gyvatukas package (maybe)"""
    meta = importlib.metadata.metadata('gyvatukas')
    if meta:
        try:
            return meta.json["version"]
        except KeyError:
            return "unknown"
    return "unknown"


def get_base_cache_path() -> pathlib.Path:
    """Returns the base cache path to save data to on end user's machine."""
    path = pathlib.Path(appdirs.user_cache_dir(appname="gyvatukas", appauthor="gyvtaukas"))
    path.mkdir(parents=True, exist_ok=True)
    return path
