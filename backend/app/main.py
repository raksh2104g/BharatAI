from fastapi import FastAPI
from backend.app.config import settings
from backend.app.api.router import router
from backend.app.database import engine, Base
from backend.app.models.user import User
from backend.app.models.document import Document
from backend.app.models.chat import Chat




Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="India's Personal AI Operating System",
    version=settings.APP_VERSION
)

# Connect all API routers
app.include_router(router)


# Home API
@app.get("/")
def home():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running Successfully 🚀"
    }