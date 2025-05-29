from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.seed import create_tables, insert_initial_data
from app.init_scripts import create_views_and_constraints
from app.wait_for_db import wait_for_db

logger = logging.getLogger(__name__)

def init_db():
    try:
        logger.info("Waiting for database to be ready...")
        wait_for_db()
        
        logger.info("Creating tables...")
        create_tables()
        
        logger.info("Inserting initial data...")
        insert_initial_data()
        
        logger.info("Creating views and constraints...")
        create_views_and_constraints()
        
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application lifespan")
    init_db()
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://localhost:5173"] para más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.routers import vehiculos
app.include_router(vehiculos.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Autos"}
