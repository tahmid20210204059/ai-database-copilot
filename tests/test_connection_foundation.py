from dotenv import load_dotenv
import os

load_dotenv(".env", override=True)

print("========== FERNET KEY TEST ==========")

key = os.getenv("FERNET_KEY")

print("FERNET_KEY exists:", bool(key))
print("FERNET_KEY length:", len(key) if key else None)


print("\n========== CONFIG TEST ==========")

from backend.app.config import settings

print("Config FERNET loaded:", bool(settings.FERNET_KEY))


print("\n========== ENCRYPTION TEST ==========")

from backend.app.utils.encryption import encryption_service

original = "DatabasePassword123"

encrypted = encryption_service.encrypt(original)

decrypted = encryption_service.decrypt(encrypted)

print("Encrypted generated:", encrypted.startswith("gAAAA"))
print("Decryption successful:", decrypted == original)


print("\n========== MODEL TEST ==========")

from backend.app.models.connection import DatabaseConnection

print("Model loaded:", DatabaseConnection.__tablename__)


print("\n========== MODEL COLUMNS ==========")

print([
    column.name
    for column in DatabaseConnection.__table__.columns
])


print("\n========== SCHEMA TEST ==========")

from backend.app.schemas.connection import ConnectionCreate

test_schema = ConnectionCreate(
    connection_name="Test Database",
    host="localhost",
    port=3306,
    database_name="enterprise_sales",
    username="copilot_reader",
    password="TestPassword123",
    ssl_enabled=False
)

print("Schema validation:", test_schema.connection_name)


print("\n========== DATABASE TABLE CHECK ==========")

from backend.app.database import app_engine
from sqlalchemy import text

connection = app_engine.connect()

result = connection.execute(
    text("SHOW TABLES LIKE 'db_connections'")
).fetchall()

print(result)

connection.close()


print("\n========== FINAL RESULT ==========")

print("DATABASE CONNECTION FOUNDATION TEST PASSED")