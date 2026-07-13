from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)





class UserRegister(BaseModel):
    """
    Registration request data.
    """

    name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=72,
    )



    @field_validator("name")
    @classmethod
    def clean_name(
        cls,
        value: str,
    ) -> str:

        cleaned_name = (
            " ".join(
                value.strip().split()
            )
        )


        if len(cleaned_name) < 2:

            raise ValueError(
                "Name must contain at least 2 characters"
            )


        return cleaned_name





    @field_validator("email")
    @classmethod
    def clean_email(
        cls,
        value: EmailStr,
    ) -> str:

        return (
            str(value)
            .strip()
            .lower()
        )





    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ) -> str:


        if not any(
            character.isalpha()
            for character in value
        ):

            raise ValueError(
                "Password must contain at least one letter"
            )



        if not any(
            character.isdigit()
            for character in value
        ):

            raise ValueError(
                "Password must contain at least one number"
            )


        return value









class UserLogin(BaseModel):
    """
    Login request data.
    """


    email: EmailStr


    password: str = Field(
        min_length=1,
        max_length=72,
    )




    @field_validator("email")
    @classmethod
    def clean_email(
        cls,
        value: EmailStr,
    ) -> str:


        return (
            str(value)
            .strip()
            .lower()
        )









class LoginUserResponse(BaseModel):
    """
    User information returned after login.
    """


    id: int

    name: str

    email: EmailStr

    role: str









class TokenResponse(BaseModel):
    """
    Login response containing JWT token
    and authenticated user information.
    """


    access_token: str

    token_type: str = "bearer"

    expires_in: int

    user: LoginUserResponse









class UserProfile(BaseModel):
    """
    Safe user information returned by API.

    Includes role information for RBAC.
    """


    model_config = ConfigDict(
        from_attributes=True
    )



    id: int

    name: str

    email: EmailStr

    role: str

    is_active: bool

    last_login_at: datetime | None

    created_at: datetime