from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from auth.config import DefaultSettings, get_settings
from auth.endpoints import list_of_routes


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Собрать 1  ендпоинтов, байндим к приложению по префиксу из настроек.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Сервис для раздачи JWT токенов"

    tags_metadata = [
        {
            "name": "Application Health",
            "description": "API health check.",
        },
    ]

    application = FastAPI(
        title="Auth service",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    settings_for_application = get_settings()

    run(
        "auth.__main__:app",
        port=settings_for_application.APP_PORT,
        host="0.0.0.0",
        reload=True,
        reload_dirs=["auth", "tests"],
        log_level="debug",
    )
