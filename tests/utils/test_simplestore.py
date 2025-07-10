import pytest
import tempfile
import shutil
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date, time
from gyvatukas.utils.simplestore import DirStore

class TestDirStore:
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def store(self, temp_dir):
        return DirStore(temp_dir)

    def test_init_creates_directory(self, temp_dir):
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        store = DirStore(temp_dir)
        assert temp_dir.exists()
        assert temp_dir.is_dir()

    def test_safe_filename_conversion(self, store):
        assert store._safe_filename("hello") == "hello"
        assert store._safe_filename("hello-world") == "hello-world"
        assert store._safe_filename("hello_world") == "hello_world"
        assert store._safe_filename("hello/world") == "hello_world"
        assert store._safe_filename("hello\\world") == "hello_world"
        assert store._safe_filename("hello:world") == "hello_world"
        assert store._safe_filename("hello@world#123") == "helloworld123"

    def test_safe_filename_validation(self, store):
        with pytest.raises(ValueError, match="Key cannot be empty"):
            store._safe_filename("")
        with pytest.raises(ValueError, match="Key cannot be empty"):
            store._safe_filename("   ")
        # Only special characters that become empty after conversion
        with pytest.raises(ValueError, match="cannot be converted to safe filename"):
            store._safe_filename("@@@")

    def test_set_and_get_basic_types(self, store):
        store.set("string_key", "hello world")
        assert store.get("string_key") == "hello world"
        store.set("int_key", 42)
        assert store.get("int_key") == 42
        store.set("float_key", 3.14)
        assert store.get("float_key") == 3.14
        store.set("bool_key", True)
        assert store.get("bool_key") is True
        store.set("none_key", None)
        assert store.get("none_key") is None

    def test_set_and_get_complex_types(self, store):
        test_list = [1, 2, 3, "hello"]
        store.set("list_key", test_list)
        assert store.get("list_key") == test_list
        test_dict = {"a": 1, "b": "hello", "c": [1, 2, 3]}
        store.set("dict_key", test_dict)
        assert store.get("dict_key") == test_dict
        test_tuple = (1, 2, "hello")
        store.set("tuple_key", test_tuple)
        assert store.get("tuple_key") == test_tuple
        test_set = {1, 2, 3, "hello"}
        store.set("set_key", test_set)
        assert store.get("set_key") == test_set
        test_frozenset = frozenset([1, 2, 3])
        store.set("frozenset_key", test_frozenset)
        assert store.get("frozenset_key") == test_frozenset

    def test_set_and_get_special_types(self, store):
        test_bytes = b"hello world"
        store.set("bytes_key", test_bytes)
        assert store.get("bytes_key") == test_bytes
        test_decimal = Decimal("19.99")
        store.set("decimal_key", test_decimal)
        assert store.get("decimal_key") == test_decimal
        test_datetime = datetime(2023, 1, 1, 12, 30, 45)
        store.set("datetime_key", test_datetime)
        assert store.get("datetime_key") == test_datetime
        test_date = date(2023, 1, 1)
        store.set("date_key", test_date)
        assert store.get("date_key") == test_date
        test_time = time(12, 30, 45)
        store.set("time_key", test_time)
        assert store.get("time_key") == test_time

    def test_set_override_behavior(self, store):
        store.set("test_key", "original_value")
        assert store.get("test_key") == "original_value"
        with pytest.raises(ValueError, match="already exists"):
            store.set("test_key", "new_value")
        store.set("test_key", "new_value", override=True)
        assert store.get("test_key") == "new_value"

    def test_get_nonexistent_key(self, store):
        assert store.get("nonexistent_key") is None

    def test_exists(self, store):
        assert store.exists("nonexistent_key") is False
        store.set("test_key", "value")
        assert store.exists("test_key") is True
        store.delete("test_key")
        assert store.exists("test_key") is False

    def test_delete(self, store):
        store.set("test_key", "value")
        assert store.exists("test_key") is True
        result = store.delete("test_key")
        assert result is True
        assert store.exists("test_key") is False
        assert store.get("test_key") is None
        result = store.delete("nonexistent_key")
        assert result is False

    def test_pop(self, store):
        store.set("test_key", "value")
        assert store.exists("test_key") is True
        popped_value = store.pop("test_key")
        assert popped_value == "value"
        assert store.exists("test_key") is False
        assert store.get("test_key") is None
        popped_value = store.pop("nonexistent_key")
        assert popped_value is None

    def test_keys(self, store):
        assert store.keys() == []
        store.set("key1", "value1")
        store.set("key2", "value2")
        store.set("key3", "value3")
        keys = store.keys()
        assert len(keys) == 3
        assert "key1" in keys
        assert "key2" in keys
        assert "key3" in keys
        store.delete("key2")
        keys = store.keys()
        assert len(keys) == 2
        assert "key1" in keys
        assert "key3" in keys
        assert "key2" not in keys

    def test_clear(self, store):
        store.set("key1", "value1")
        store.set("key2", "value2")
        store.set("key3", "value3")
        assert len(store.keys()) == 3
        store.clear()
        assert store.keys() == []
        assert store.get("key1") is None
        assert store.get("key2") is None
        assert store.get("key3") is None

    def test_get_info(self, store):
        assert store.get_info("nonexistent_key") is None
        store.set("test_key", "test_value")
        info = store.get_info("test_key")
        assert info is not None
        assert "type" in info
        assert "encoding" in info
        assert "size_bytes" in info
        assert info["type"] == "str"
        assert info["encoding"] == "json"
        assert info["size_bytes"] > 0

    def test_corrupted_data_handling(self, store):
        store.set("test_key", "test_value")
        data_file, meta_file = store._get_file_paths("test_key")
        with open(data_file, "w") as f:
            f.write("invalid json")
        assert store.get("test_key") is None

    def test_corrupted_metadata_handling(self, store):
        store.set("test_key", "test_value")
        data_file, meta_file = store._get_file_paths("test_key")
        with open(meta_file, "w") as f:
            f.write("invalid json")
        assert store.get("test_key") is None

    def test_missing_metadata_file(self, store):
        store.set("test_key", "test_value")
        data_file, meta_file = store._get_file_paths("test_key")
        meta_file.unlink()
        assert store.get("test_key") is None

    def test_missing_data_file(self, store):
        store.set("test_key", "test_value")
        data_file, meta_file = store._get_file_paths("test_key")
        data_file.unlink()
        assert store.get("test_key") is None

    def test_nested_data_structures(self, store):
        nested_data = {
            "level1": {
                "level2": {
                    "level3": [1, 2, 3, {"nested": "value"}]
                }
            },
            "list_with_dicts": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        store.set("nested_key", nested_data)
        retrieved = store.get("nested_key")
        assert retrieved == nested_data
        assert retrieved["level1"]["level2"]["level3"][3]["nested"] == "value"
        assert retrieved["list_with_dicts"][1]["name"] == "Bob"

    def test_large_data_handling(self, store):
        large_list = list(range(1000))
        large_dict = {f"key_{i}": f"value_{i}" for i in range(100)}
        store.set("large_list", large_list)
        store.set("large_dict", large_dict)
        retrieved_list = store.get("large_list")
        retrieved_dict = store.get("large_dict")
        assert retrieved_list == large_list
        assert retrieved_dict == large_dict
        assert len(retrieved_list) == 1000
        assert len(retrieved_dict) == 100

    def test_special_characters_in_keys(self, store):
        special_keys = [
            "key/with/slashes",
            "key\\with\\backslashes",
            "key:with:colons",
            "key@with@symbols",
            "key#with#hashes",
            "key with spaces",
            "key.with.dots"
        ]
        for i, key in enumerate(special_keys):
            store.set(key, f"value_{i}")
            assert store.get(key) == f"value_{i}"
            assert store.exists(key) is True

    def test_concurrent_access_simulation(self, store):
        operations = [
            ("set", "key1", "value1"),
            ("set", "key2", "value2"),
            ("get", "key1", None),
            ("exists", "key2", None),
            ("set", "key3", "value3"),
            ("delete", "key1", None),
            ("get", "key1", None),
            ("pop", "key2", None),
            ("clear", None, None)
        ]
        results = []
        for op, key, value in operations:
            if op == "set":
                store.set(key, value)
                results.append(None)
            elif op == "get":
                results.append(store.get(key))
            elif op == "exists":
                results.append(store.exists(key))
            elif op == "delete":
                results.append(store.delete(key))
            elif op == "pop":
                results.append(store.pop(key))
            elif op == "clear":
                store.clear()
                results.append(None)
        assert results[2] == "value1"
        assert results[3] is True
        assert results[5] is True
        assert results[6] is None
        assert results[7] == "value2" 