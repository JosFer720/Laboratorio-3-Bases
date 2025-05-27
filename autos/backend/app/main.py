from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
import logging
from app.seed import init_db

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicializando base de datos...")
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error inicializando DB: {e}")
        raise
    
    yield  
    
    logger.info("Cerrando aplicación...")

app = FastAPI(lifespan=lifespan)

from app.routers import vehiculos
app.include_router(vehiculos.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Autos"}