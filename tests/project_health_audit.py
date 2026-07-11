import sys
import os
from pathlib import Path

errors = []


def ok(message):
    print("[OK]", message)


def fail(message, error=None):
    print("[FAILED]", message)

    if error:
        print("   ", error)

    errors.append(message)


print("\n========== ENVIRONMENT ==========")

try:
    print("Python:", sys.version.split()[0])

    if "venv" in sys.executable.lower():
        ok("Virtual environment active")
    else:
        fail("Virtual environment not active")

except Exception as e:
    fail("Environment check failed", e)



print("\n========== PROJECT FILE STRUCTURE ==========")

required_files = [

    "backend/app/main.py",
    "backend/app/config.py",

    "backend/app/database/__init__.py",
    "backend/app/database/base.py",
    "backend/app/database/session.py",
    "backend/app/database/dynamic_engine.py",

    "backend/app/models/user.py",
    "backend/app/models/connection.py",

    "backend/app/schemas/auth.py",
    "backend/app/schemas/connection.py",

    "backend/app/auth/password.py",
    "backend/app/auth/jwt_handler.py",

    "backend/app/services/connection_service.py",

    "backend/app/utils/encryption.py",

]


for file in required_files:

    if Path(file).exists():
        ok(file)

    else:
        fail(f"Missing {file}")



print("\n========== CONFIG TEST ==========")

try:

    from backend.app.config import settings

    ok("Config imported")

    print("APP DATABASE:", bool(settings.APP_DATABASE_URL))
    print("READER DATABASE:", bool(settings.READER_DATABASE_URL))
    print("JWT:", bool(settings.JWT_SECRET_KEY))
    print("FERNET:", bool(settings.FERNET_KEY))

except Exception as e:

    fail("Config failed", e)



print("\n========== DATABASE PACKAGE TEST ==========")

try:

    from backend.app.database import (
        Base,
        app_engine,
        reader_engine,
        get_app_db,
        get_reader_db,
        check_database_connection,
        create_dynamic_engine,
    )

    ok("Database package import")

    ok("SQLAlchemy Base loaded")

    ok("App engine loaded")

    ok("Reader engine loaded")

    ok("Dynamic engine loaded")


except Exception as e:

    fail("Database package failed", e)



print("\n========== DATABASE CONNECTION TEST ==========")

try:

    from sqlalchemy import text
    from backend.app.database import (
        app_engine,
        reader_engine
    )


    with app_engine.connect() as c:

        db = c.execute(
            text("SELECT DATABASE()")
        ).scalar()

        users = c.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar()


    ok(
        f"Application DB connected: {db}"
    )

    ok(
        f"Users table accessible: {users} rows"
    )



    with reader_engine.connect() as c:

        db = c.execute(
            text("SELECT DATABASE()")
        ).scalar()

        customers = c.execute(
            text("SELECT COUNT(*) FROM customers")
        ).scalar()


    ok(
        f"Reader DB connected: {db}"
    )

    ok(
        f"Customers table accessible: {customers} rows"
    )


except Exception as e:

    fail("Database connection failed", e)



print("\n========== MODEL TEST ==========")

try:

    from backend.app.models.user import User
    from backend.app.models.connection import DatabaseConnection


    ok(
        f"User model: {User.__tablename__}"
    )

    ok(
        f"Connection model: {DatabaseConnection.__tablename__}"
    )


    print(
        "Connection columns:",
        [
            c.name
            for c in DatabaseConnection.__table__.columns
        ]
    )


except Exception as e:

    fail("Model test failed", e)



print("\n========== SCHEMA TEST ==========")

try:

    from backend.app.schemas.auth import UserRegister

    from backend.app.schemas.connection import (
        ConnectionCreate
    )


    user = UserRegister(
        name="Audit User",
        email="audit@test.com",
        password="Password123"
    )


    connection = ConnectionCreate(
        connection_name="Audit DB",
        host="localhost",
        port=3306,
        database_name="enterprise_sales",
        username="copilot_reader",
        password="Password123"
    )


    ok("Auth schema validation")

    ok("Connection schema validation")


except Exception as e:

    fail("Schema test failed", e)



print("\n========== SECURITY TEST ==========")

try:

    from backend.app.utils.encryption import (
        encryption_service
    )


    original = "SecretPassword123"

    encrypted = encryption_service.encrypt(
        original
    )

    decrypted = encryption_service.decrypt(
        encrypted
    )


    if encrypted != original:

        ok("Password encryption working")


    if decrypted == original:

        ok("Password decryption working")


except Exception as e:

    fail("Encryption failed", e)



print("\n========== AUTH TEST ==========")

try:

    from backend.app.auth.password import (
        hash_password,
        verify_password
    )


    hashed = hash_password(
        "TestPassword123"
    )


    if verify_password(
        "TestPassword123",
        hashed
    ):

        ok("Bcrypt working")


except Exception as e:

    fail("Authentication test failed", e)



print("\n========== FASTAPI TEST ==========")

try:

    from backend.app.main import app


    ok(
        "FastAPI application imported"
    )


    print(
        "Routes:"
    )


    for route in app.routes:

        print(
            " -",
            getattr(
                route,
                "path",
                type(route).__name__
            )
        )


except Exception as e:

    fail("FastAPI failed", e)



print("\n========== FINAL RESULT ==========")


if errors:

    print(
        "FAILED:",
        len(errors),
        "issue(s)"
    )

    for e in errors:
        print("-", e)

    sys.exit(1)


else:

    print(
        "ALL SYSTEM CHECKS PASSED"
    )