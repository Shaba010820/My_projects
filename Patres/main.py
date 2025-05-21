from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import engine
from app.models.user import Base
from app.routers.auth import router as auth_router
from app.routers.books import router as books_router
from app.routers.borrow import router as borrow_router
from app.routers.readers import router as reader_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(borrow_router)
app.include_router(books_router)
app.include_router(reader_router)
