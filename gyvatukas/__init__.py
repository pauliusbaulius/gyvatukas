"""
.. include:: ../README.md
"""
from .utils.bool import is_true, value_to_bool
from .utils.crypto import is_psw_correct, get_hashed_salted_password
from .utils.dict_ import dict_remove_matching_values
from .utils.dt import get_dt_utc_now
from .utils.env import get_env
from .utils.fs import (
    path_without_filename,
    path_extension,
    path_filename,
    dir_exists,
    file_exists,
    write_file,
    read_file,
    ScanResultSchema,
    scan_dir,
)
from .utils.generators import get_random_secure_string
from .utils.ip import get_my_ipv4, get_ipv4_meta, get_ip_country
from .utils.json_ import get_pretty_json, read_json, write_json, load_json
from .utils.lithuania import (
    LithuanianPersonalCodeSchema,
    validate_lt_id,
    validate_lt_tel_nr,
)
from .utils.optimization import compress_data, decompress_data
from .utils.validators import is_email_valid

__all__ = [
    # bool.py
    "is_true",
    "value_to_bool",
    # crypo.py
    "is_psw_correct",
    "get_hashed_salted_password",
    # dict_.py
    "dict_remove_matching_values",
    # dt.py
    "get_dt_utc_now",
    # env.py
    "get_env",
    # fs.py
    "path_without_filename",
    "path_extension",
    "path_filename",
    "dir_exists",
    "file_exists",
    "write_file",
    "read_file",
    "ScanResultSchema",
    "scan_dir",
    # generators.py
    "get_random_secure_string",
    # ip.py
    "get_my_ipv4",
    "get_ipv4_meta",
    "get_ip_country",
    # json_.py
    "get_pretty_json",
    "read_json",
    "write_json",
    "load_json",
    # lithuania.py
    "LithuanianPersonalCodeSchema",
    "validate_lt_id",
    "validate_lt_tel_nr",
    # optimization.py
    "compress_data",
    "decompress_data",
    # validators.py
    "is_email_valid",
]
