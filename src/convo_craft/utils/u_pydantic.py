"""Utils for the pydantic module."""

from pydantic import SecretStr as SecretStrV2
from pydantic.v1 import SecretStr as SecretStrV1


def convert_to_secret_str(value: SecretStrV1 | str) -> SecretStrV1:
    """Convert a string to a SecretStr if needed.

    Args:
        value (SecretStr | str): The value to convert.

    Returns:
        SecretStr: The SecretStr value.
    """
    if isinstance(value, SecretStrV1):
        return value
    return SecretStrV1(value)


def convert_to_secret_str_v2(value: SecretStrV2 | str) -> SecretStrV2:
    """Convert a string to a SecretStr if needed.

    Args:
        value (SecretStr | str): The value to convert.

    Returns:
        SecretStr: The SecretStr value.
    """
    if isinstance(value, SecretStrV2):
        return value
    return SecretStrV2(value)
