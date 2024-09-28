"""Utils for the pydantic module."""

from pydantic.v1 import SecretStr


def convert_to_secret_str(value: SecretStr | str) -> SecretStr:
    """Convert a string to a SecretStr if needed.

    Args:
        value (SecretStr | str): The value to convert.

    Returns:
        SecretStr: The SecretStr value.
    """
    if isinstance(value, SecretStr):
        return value
    return SecretStr(value)
