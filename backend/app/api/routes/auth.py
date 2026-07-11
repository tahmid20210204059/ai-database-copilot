from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from ...auth.jwt_handler import (
    create_access_token,
    get_current_user,
)
from ...auth.password import (
    hash_password,
    verify_password,
)
from ...database import get_app_db
from ...models.user import User
from ...schemas.auth import (
    TokenResponse,
    UserLogin,
    UserProfile,
    UserRegister,
)


router = APIRouter(
    prefix="/api",
    tags=["Authentication"],
)


# Unknown email এবং wrong password-এর response timing
# কাছাকাছি রাখার জন্য dummy hash
DUMMY_PASSWORD_HASH = "$2b$12$KIXQ9XJ7w9F5Y0pX5k7Y8eJ4vZJ8jK1wFq8V1mZ8nZ7u8xQ0xYqK2"


@router.post(
    "/register",
    response_model=UserProfile,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserRegister,
    database: Session = Depends(get_app_db),
) -> User:
    """নতুন application user register করবে."""

    email = str(payload.email).lower()

    existing_user = database.scalar(
        select(User).where(User.email == email)
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    new_user = User(
        name=payload.name,
        email=email,
        password_hash=hash_password(payload.password),
        is_active=True,
    )

    try:
        database.add(new_user)
        database.commit()
        database.refresh(new_user)

    except IntegrityError:
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    except SQLAlchemyError:
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user account",
        )

    return new_user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    payload: UserLogin,
    database: Session = Depends(get_app_db),
) -> TokenResponse:
    """Email এবং password দিয়ে login করবে."""

    email = str(payload.email).lower()

    user = database.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        verify_password(
            payload.password,
            DUMMY_PASSWORD_HASH,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    user.last_login_at = (
        datetime.now(timezone.utc).replace(tzinfo=None)
    )

    try:
        database.commit()
        database.refresh(user)

    except SQLAlchemyError:
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to complete login",
        )

    access_token, expires_in = create_access_token(
        user_id=user.id,
        email=user.email,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
    )


@router.get(
    "/profile",
    response_model=UserProfile,
)
def get_profile(
    current_user: User = Depends(get_current_user),
) -> User:
    """বর্তমানে login করা user-এর profile return করবে."""

    return current_user