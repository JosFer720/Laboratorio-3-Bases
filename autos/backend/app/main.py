from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.seed import create_tables, insert_initial_data
from app.init_scripts import create_views_and_constraints

logger = logging.getLogger(__name__)

def init_db():
    logger.info("Inicializando base de datos...")
    try:
        create_tables()
        insert_initial_data()
        create_views_and_constraints()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    logger.info("Cerrando aplicación...")

app = FastAPI(lifespan=lifespan)

from app.routers import vehiculos
app.include_router(vehiculos.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Autos"}
