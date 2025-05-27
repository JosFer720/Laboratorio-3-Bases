from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.seed import init_db
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Inicializando base de datos...")
        init_db()
        logger.info("Base de datos lista")
    except Exception as e:
        logger.error(f"Error inicializando DB: {e}")
        raise

    yield

app = FastAPI(lifespan=lifespan)

from app.routers import vehiculos
app.include_router(vehiculos.router)
