from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .api.routes.connections import (
    router as connection_router,
)

from .api.routes.schema import (
    router as schema_router,
)

from .api.routes.history import (
    router as history_router,
)

from .api.routes.auth import (
    router as auth_router,
)

from .api.routes.ai import (
    router as ai_router,
)

from .api.routes.explanation import (
    router as explanation_router,
)

from .api.routes.admin import (
    router as admin_router,
)



from .config import settings


from .database import (
    app_engine,
    check_database_connection,
    reader_engine,
)



from .api.routes.user import (
    router as user_router
)



app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP.VERSION
    if hasattr(settings, "APP_VERSION") is False
    else settings.APP_VERSION,

    description=(

        "Convert natural language into safe SQL, execute queries, "
        "explain results and generate visualizations."

    ),

)







app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://127.0.0.1:5500",

        "http://localhost:5500",

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)









app.include_router(
    auth_router
)

app.include_router(
    connection_router
)

app.include_router(
    schema_router
)

app.include_router(
    ai_router
)

app.include_router(
    history_router
)

app.include_router(
    explanation_router
)

app.include_router(
    admin_router
)









@app.get(
    "/",
    tags=["General"],
)
def home() -> dict:

    return {

        "message":
        settings.APP_NAME,

        "version":
        settings.APP_VERSION,

    }









@app.get(
    "/health",
    tags=["Health"],
)
def health_check() -> dict:

    return {

        "status":
        "healthy",

        "service":
        settings.APP_NAME,

    }









@app.get(
    "/health/databases",
    tags=["Health"],
)
def database_health_check() -> dict:


    app_database_result = (
        check_database_connection(
            app_engine
        )
    )


    reader_database_result = (
        check_database_connection(
            reader_engine
        )
    )



    app_connected = (
        app_database_result["status"]
        ==
        "connected"
    )



    reader_connected = (
        reader_database_result["status"]
        ==
        "connected"
    )



    overall_status = (

        "healthy"

        if app_connected and reader_connected

        else

        "degraded"

    )



    return {

        "status":
        overall_status,


        "app_database":
        app_database_result["status"],


        "reader_database":
        reader_database_result["status"],



        "details": {

            "app_database":
            app_database_result,


            "reader_database":
            reader_database_result,

        },

    }

app.include_router(
    user_router
)