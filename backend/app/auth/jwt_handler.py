from datetime import (
    datetime,
    timedelta,
    timezone,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from jose import (
    JWTError,
    jwt,
)

from sqlalchemy.orm import Session


from ..config import settings

from ..database import get_app_db

from ..models.user import User





bearer_scheme = HTTPBearer(
    auto_error=False
)







def create_access_token(
    user_id: int,
    email: str,
    role: str,
) -> tuple[str, int]:
    """
    Create signed JWT access token.

    JWT contains:
    - user id
    - email
    - role
    """



    expires_in_seconds = (
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
        * 60
    )



    issued_at = datetime.now(
        timezone.utc
    )


    expires_at = (
        issued_at
        +
        timedelta(
            minutes=
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )



    token_payload = {

        "sub":
        str(user_id),


        "email":
        email,


        "role":
        role,


        "type":
        "access",


        "iat":
        issued_at,


        "exp":
        expires_at,

    }






    access_token = jwt.encode(

        token_payload,

        settings.JWT_SECRET_KEY,

        algorithm=
        settings.JWT_ALGORITHM,

    )



    return (
        access_token,
        expires_in_seconds,
    )









def unauthorized_exception(
    detail: str =
    "Could not validate credentials",
) -> HTTPException:


    return HTTPException(

        status_code=
        status.HTTP_401_UNAUTHORIZED,


        detail=
        detail,


        headers={
            "WWW-Authenticate":
            "Bearer"
        },

    )









def get_current_user(
    credentials:
    HTTPAuthorizationCredentials | None =
    Depends(
        bearer_scheme
    ),

    database:
    Session =
    Depends(
        get_app_db
    ),

) -> User:
    """
    Authenticate user from JWT token.
    """



    if credentials is None:

        raise unauthorized_exception(
            "Authentication token is required"
        )





    if credentials.scheme.lower() != "bearer":

        raise unauthorized_exception(
            "Invalid authentication scheme"
        )





    token = credentials.credentials




    try:


        payload = jwt.decode(

            token,

            settings.JWT_SECRET_KEY,

            algorithms=[
                settings.JWT_ALGORITHM
            ],

        )



        if payload.get(
            "type"
        ) != "access":


            raise unauthorized_exception(
                "Invalid token type"
            )





        subject = payload.get(
            "sub"
        )



        if subject is None:

            raise unauthorized_exception()



        user_id = int(
            subject
        )




    except (
        JWTError,
        ValueError,
    ):

        raise unauthorized_exception()





    user = database.get(
        User,
        user_id,
    )



    if user is None:

        raise unauthorized_exception(
            "User account was not found"
        )





    if not user.is_active:

        raise HTTPException(

            status_code=
            status.HTTP_403_FORBIDDEN,


            detail=
            "User account is inactive",

        )



    return user