from passlib.context import CryptContext


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash plain password using bcrypt.
    bcrypt supports maximum 72 bytes.
    """

    password = password[:72]

    return password_context.hash(password)


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    """
    Verify password against stored hash.
    """

    plain_password = plain_password[:72]

    return password_context.verify(
        plain_password,
        password_hash,
    )