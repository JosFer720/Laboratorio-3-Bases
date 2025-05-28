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
        logger.info("✅ Tablas creadas")
        insert_initial_data()
        logger.info("✅ Datos insertados")
        create_views_and_constraints()
        logger.info("✅ Vistas y restricciones creadas")
    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🟡 Entrando a lifespan")
    init_db()
    print("🟢 Base de datos lista")
    yield
    print("🔴 Cerrando app")


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
