from backend.app.database import app_engine
from sqlalchemy import text


connection = app_engine.connect()

result = connection.execute(
    text(
        "SHOW TABLES LIKE 'query_history'"
    )
).fetchall()


print(result)


connection.close()