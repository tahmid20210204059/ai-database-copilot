from passlib.context import CryptContext


password_context = CryptContext(
    schemes=[
        "bcrypt"
    ],
    deprecated="auto",
)



MAX_PASSWORD_LENGTH = 72



def _normalize_password(
    password: str
) -> str:
    """
    Normalize password before hashing
    and verification.

    bcrypt supports maximum 72 bytes.
    """

    if not password:

        raise ValueError(
            "Password cannot be empty"
        )


    return password[:MAX_PASSWORD_LENGTH]





def hash_password(
    password: str
) -> str:
    """
    Hash plain password using bcrypt.

    Used during:
    - User registration
    - Admin/Owner creation
    """

    password = _normalize_password(
        password
    )


    return password_context.hash(
        password
    )





def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    """
    Verify plain password against
    stored bcrypt hash.
    """


    plain_password = _normalize_password(
        plain_password
    )


    return password_context.verify(
        plain_password,
        password_hash,
    )