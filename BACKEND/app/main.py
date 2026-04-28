from fastapi import FastAPI
from app.routers import user_router
from app.routers import room_router
from app.routers import auth_router
from app.routers import ai_router
from app.db.session import engine
from app.db.base import Base
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.cache.client import connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    await connection.aclose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # libera qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # libera todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # libera todos os headers
)

# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)


app.include_router(user_router.router)
app.include_router(room_router.router)
app.include_router(auth_router.router)
app.include_router(ai_router.router)
