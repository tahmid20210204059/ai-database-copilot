"""
Create initial owner account
for AI Database Copilot.

Usage:

python -m backend.app.scripts.create_owner
"""


from sqlalchemy.orm import Session

from ..database.session import AppSessionLocal

from ..models.user import User

from ..auth.password import hash_password





OWNER_NAME = "Admin"

OWNER_EMAIL = "admin@copilot.com"

OWNER_PASSWORD = "Admin12345"





def create_owner(
    database: Session
):

    existing_user = (
        database.query(User)
        .filter(
            User.email == OWNER_EMAIL
        )
        .first()
    )


    if existing_user:

        print(
            "Owner user already exists:"
        )

        print(
            existing_user.email
        )

        return




    owner = User(

        name=OWNER_NAME,

        email=OWNER_EMAIL,

        password_hash=
        hash_password(
            OWNER_PASSWORD
        ),

        role="owner",

        is_active=True,

    )



    database.add(owner)

    database.commit()

    database.refresh(
        owner
    )



    print(
        "Owner user created successfully"
    )


    print(
        f"ID: {owner.id}"
    )


    print(
        f"Email: {owner.email}"
    )


    print(
        "Role: owner"
    )






def main():

    database = AppSessionLocal()


    try:

        create_owner(
            database
        )


    finally:

        database.close()





if __name__ == "__main__":

    main()