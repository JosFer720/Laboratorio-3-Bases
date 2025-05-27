import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def wait_for_db():
    DATABASE_URL = "postgresql://autos_user:autos_pass@db:5432/autos_db"
    engine = create_engine(DATABASE_URL)
    
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                logger.info("Conexión a la base de datos establecida")
                return True
        except OperationalError as e:
            if attempt == max_retries - 1:
                logger.error(f"Error de conexión después de {max_retries} intentos: {e}")
                raise
            logger.warning(f"Intento {attempt + 1} de {max_retries}: DB no disponible, reintentando en {retry_delay}s...")
            time.sleep(retry_delay)

if __name__ == "__main__":
    wait_for_db()