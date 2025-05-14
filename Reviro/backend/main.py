from fastapi import FastAPI
from .routers.crud import router
from .routers.auth import router as auth_router
from .models.models import BaseModel
from .database.session import engine

app = FastAPI()

@app.on_event('startup')
def on_startup():
    BaseModel.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(auth_router)

