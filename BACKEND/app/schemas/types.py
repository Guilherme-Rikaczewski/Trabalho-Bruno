from pydantic import StringConstraints, AfterValidator
from typing import Annotated


def validate_password(password: str) -> str:
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain a lowercase letter")

    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain an uppercase letter")

    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain a number")

    return password


Username = Annotated[
    str,
    StringConstraints(
        max_length=20,
        min_length=1,
        strip_whitespace=True,
    )
]

Password = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=50,
        strip_whitespace=True,
    ),
    AfterValidator(validate_password)
]

RoomName = Annotated[
    str,
    StringConstraints(
        max_length=100,
        min_length=1,
        strip_whitespace=True,
    )
]

RoomCode = Annotated[
    str,
    StringConstraints(
        max_length=6,
        min_length=6,
        strip_whitespace=True,
        to_upper=True,
    )
]
