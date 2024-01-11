import json
import subprocess

import zstandard as zstd

TYPE_COMPRESSIBLE_DATA_TYPES = bytes | str | list | dict

# TODO: Use gzip if zstd not found.


def _is_zstd_installed() -> bool:
    """Check if zstd is installed."""
    try:
        subprocess.run(
            ["zstd", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def compress_data(data: TYPE_COMPRESSIBLE_DATA_TYPES) -> tuple[bytes, float]:
    """Compress data using zstd.

    Return compressed data and compression ratio (smaller is better aka 0.1 ratio means data is 1/10 of the og size).
    """
    if isinstance(data, (dict, list)):
        data = json.dumps(data)

    # Encode the string to bytes
    if isinstance(data, str):
        data = data.encode("utf-8")

    og_size = len(data)

    z = zstd.ZstdCompressor(level=3)
    compressed_data = z.compress(data)

    comp_size = len(compressed_data)
    ratio = round(comp_size / og_size, 2)

    return compressed_data, ratio


def decompress_data(data: bytes) -> TYPE_COMPRESSIBLE_DATA_TYPES:
    """Decompress data using zstd."""
    z = zstd.ZstdDecompressor()
    decompressed_data = z.decompress(data)

    # Decode bytes to string
    data = decompressed_data.decode("utf-8")

    # Try to convert back to list/dict.
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        pass

    return data
