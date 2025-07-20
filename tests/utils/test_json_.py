import pytest
import decimal
import datetime
from gyvatukas.utils.json_ import json_dumps_safe


@pytest.mark.parametrize(
    "input_data,expected_json",
    [
        pytest.param(input_data, expected_json, id=f"case_{i}")
        for i, (input_data, expected_json) in enumerate(
            [
                # Basic types
                (
                    {"string": "hello", "number": 42, "boolean": True, "null": None},
                    '{"string": "hello", "number": 42, "boolean": true, "null": null}',
                ),
                # Decimal conversion
                ({"decimal": decimal.Decimal("123.45")}, '{"decimal": "123.45"}'),
                # Datetime conversion
                (
                    {"datetime": datetime.datetime(2023, 1, 1, 12, 30, 45)},
                    '{"datetime": "2023-01-01T12:30:45"}',
                ),
                # Date conversion
                ({"date": datetime.date(2023, 1, 1)}, '{"date": "2023-01-01"}'),
                # Non-string keys conversion
                (
                    {123: "integer_key", True: "boolean_key", None: "none_key"},
                    '{"123": "integer_key", "True": "boolean_key", "None": "none_key"}',
                ),
                # Decimal keys
                ({decimal.Decimal("1.5"): "decimal_key"}, '{"1.5": "decimal_key"}'),
                # Datetime keys
                (
                    {datetime.datetime(2023, 1, 1): "datetime_key"},
                    '{"2023-01-01T00:00:00": "datetime_key"}',
                ),
                # Nested structures
                (
                    {
                        "nested": {
                            "decimal": decimal.Decimal("999.99"),
                            "datetime": datetime.datetime(2023, 12, 31, 23, 59, 59),
                        }
                    },
                    '{"nested": {"decimal": "999.99", "datetime": "2023-12-31T23:59:59"}}',
                ),
                # Lists with special types
                (
                    {"list": [1, "string", True, None, decimal.Decimal("67.89")]},
                    '{"list": [1, "string", true, null, "67.89"]}',
                ),
                # Empty structures
                (
                    {"empty_dict": {}, "empty_list": [], "empty_string": ""},
                    '{"empty_dict": {}, "empty_list": [], "empty_string": ""}',
                ),
                # Complex nested structures
                (
                    {
                        "list_of_dicts": [
                            {"id": 1, "decimal": decimal.Decimal("10.5")},
                            {
                                "id": 2,
                                "datetime": datetime.datetime(2023, 6, 15, 10, 30),
                            },
                        ]
                    },
                    '{"list_of_dicts": [{"id": 1, "decimal": "10.5"}, {"id": 2, "datetime": "2023-06-15T10:30:00"}]}',
                ),
                # Mixed complex data
                (
                    {
                        "dict_of_lists": {
                            "numbers": [decimal.Decimal("1.1"), decimal.Decimal("2.2")],
                            "dates": [
                                datetime.date(2023, 1, 1),
                                datetime.date(2023, 12, 31),
                            ],
                        }
                    },
                    '{"dict_of_lists": {"numbers": ["1.1", "2.2"], "dates": ["2023-01-01", "2023-12-31"]}}',
                ),
                # pathlib.Path as value
                (
                    {"path": __import__("pathlib").Path("/tmp/test.txt")},
                    '{"path": "/tmp/test.txt"}',
                ),
                # pathlib.Path as key
                (
                    {__import__("pathlib").Path("/tmp/test.txt"): "file"},
                    '{"/tmp/test.txt": "file"}',
                ),
                # pathlib.Path in nested structure
                (
                    {"files": [__import__("pathlib").Path("/tmp/a.txt"), __import__("pathlib").Path("/tmp/b.txt")]},
                    '{"files": ["/tmp/a.txt", "/tmp/b.txt"]}',
                ),
            ]
        )
    ],
)
def test_json_dumps_safe(input_data, expected_json):
    result = json_dumps_safe(input_data)
    assert result == expected_json
