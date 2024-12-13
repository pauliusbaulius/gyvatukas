TRUE_VALUES: set = {"true", "1", "yes", "y"}


def is_true(value: str) -> bool:
    """Return whether value is true/1/yes/y."""
    return value.lower() in TRUE_VALUES


def value_to_bool(value: str) -> bool:
    return is_true(value)
