from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router


def make_application(title="Phresh"):
    app = FastAPI(title=title, version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True
    )
    app.include_router(api_router,prefix="/api")
    return app

app = make_application()