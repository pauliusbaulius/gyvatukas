from abc import ABC, abstractmethod
import os
import json
from typing import Union, Dict, List, Optional

# Type alias for supported value types
ValueType = Union[str, int, dict, list, bytes]


class AbstractDB(ABC):
    """Abstract base class for simple database implementations."""

    def __init__(self, base_path: str):
        """Initialize the database with a base path.

        Args:
            base_path: The base directory path for the database
        """
        self.base_path = os.path.abspath(base_path)
        os.makedirs(self.base_path, exist_ok=True)

    @abstractmethod
    def get(self, key: str) -> Optional[ValueType]:
        """Retrieve a value by key.

        Args:
            key: The key to look up

        Returns:
            The value if found, None if not found
        """
        pass

    @abstractmethod
    def set(self, key: str, value: ValueType) -> None:
        """Set a value for a key.

        Args:
            key: The key to set
            value: The value to store
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a key-value pair.

        Args:
            key: The key to delete

        Returns:
            True if the key was deleted, False if it didn't exist
        """
        pass

    @abstractmethod
    def update(self, key: str, value: ValueType) -> bool:
        """Update an existing key-value pair.

        Args:
            key: The key to update
            value: The new value

        Returns:
            True if the key was updated, False if it didn't exist
        """
        pass


class DirDB(AbstractDB):
    """Implementation that stores each value in a separate file."""

    def _get_path(self, key: str) -> str:
        """Get the full file path for a key."""
        safe_key = key.replace('/', '_').replace('\\', '_')
        return os.path.join(self.base_path, safe_key)

    def get(self, key: str) -> Optional[ValueType]:
        path = self._get_path(key)
        if not os.path.exists(path):
            return None

        with open(path, 'rb') as f:
            content = f.read()

        # Try to decode as string first
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return content

    def set(self, key: str, value: ValueType) -> None:
        path = self._get_path(key)

        if isinstance(value, (dict, list)):
            content = json.dumps(value).encode('utf-8')
        elif isinstance(value, int):
            content = str(value).encode('utf-8')
        elif isinstance(value, str):
            content = value.encode('utf-8')
        elif isinstance(value, bytes):
            content = value
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

        with open(path, 'wb') as f:
            f.write(content)

    def delete(self, key: str) -> bool:
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def update(self, key: str, value: ValueType) -> bool:
        if not os.path.exists(self._get_path(key)):
            return False
        self.set(key, value)
        return True


class JsonDB(AbstractDB):
    """Implementation that stores all values in a single JSON file."""

    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.db_path = os.path.join(self.base_path, 'db.json')
        self._data: Dict[str, ValueType] = {}

        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                self._data = json.load(f)

    def _save(self) -> None:
        """Save the current state to the JSON file."""
        with open(self.db_path, 'w') as f:
            json.dump(self._data, f, indent=2)

    def get(self, key: str) -> Optional[ValueType]:
        return self._data.get(key)

    def set(self, key: str, value: ValueType) -> None:
        if isinstance(value, bytes):
            raise ValueError("JsonDB doesn't support bytes values")
        self._data[key] = value
        self._save()

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def update(self, key: str, value: ValueType) -> bool:
        if key not in self._data:
            return False
        self.set(key, value)
        return True
