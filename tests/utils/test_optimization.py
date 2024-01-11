import logging
import pathlib
import json
import pytest
from gyvatukas.utils.optimization import compress_data, decompress_data

_logger = logging.getLogger("gyvatukas.test")


@pytest.mark.parametrize(
    "data",
    [
        "foo",
        {"foo": "bar"},
        ["foo", "bar"],
    ],
)
def test_compression(data) -> None:
    compressed, ratio = compress_data(data)
    _logger.debug(f"Compression ratio {ratio}.")
    decompressed = decompress_data(compressed)
    assert data == decompressed


@pytest.mark.parametrize(
    "path_to_data, data_type",
    [
        # https://microsoftedge.github.io/Demos/json-dummy-data/1MB.json
        (pathlib.Path(__file__).parent.parent / "assets" / "bigdata.json", "json"),
    ],
)
def test_compression_from_file(path_to_data, data_type) -> None:
    data = path_to_data.read_text()

    if data_type == "json":
        data = json.loads(data)

    compressed, ratio = compress_data(data)
    _logger.debug(f"Compression ratio {ratio}.")
    decompressed = decompress_data(compressed)
    assert data == decompressed
