import importlib.metadata
import pathlib
from platformdirs import user_data_dir


def get_gyvatukas_version() -> str:
    """Returns the version of the gyvatukas package (maybe)"""
    meta = importlib.metadata.metadata("gyvatukas")
    if meta:
        try:
            return meta.json["version"]
        except KeyError:
            return "unknown"
    return "unknown"


def get_base_cache_path() -> pathlib.Path:
    """Returns the base cache path to save data to on end user's machine."""
    path = pathlib.Path(
        user_data_dir(appname="gyvatukas", appauthor="gyvtaukas")
    )
    path.mkdir(parents=True, exist_ok=True)
    return path
