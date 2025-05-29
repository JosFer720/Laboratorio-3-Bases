from sqlalchemy import text
from app.database import engine
import logging

logger = logging.getLogger(__name__)

def create_views_and_constraints():
    try:
        with engine.connect() as conn:
            # Check if view exists first
            view_exists = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 FROM pg_views 
                    WHERE viewname = 'vista_vehiculos'
                )
            """)).scalar()

            if not view_exists:
                logger.info("Creating vista_vehiculos view...")
                conn.execute(text("""
                    CREATE VIEW vista_vehiculos AS
                    SELECT
                        v.id,
                        v.modelo,
                        v.anio,
                        v.precio,
                        v.tipo,
                        v.descripcion,
                        m.nombre AS marca,
                        u.nombre AS vendedor,
                        v.disponible,
                        v.fecha_publicacion,
                        STRING_AGG(c.nombre, ', ') AS categorias
                    FROM vehiculos v
                    JOIN marcas m ON v.marca_id = m.id
                    JOIN usuarios u ON v.vendedor_id = u.id
                    LEFT JOIN vehiculo_categoria vc ON vc.vehiculo_id = v.id
                    LEFT JOIN categorias c ON c.id = vc.categoria_id
                    GROUP BY v.id, m.nombre, u.nombre
                """))
                conn.commit()
                logger.info("View created successfully")

            # Constraints también deben ir dentro del bloque
            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'chk_anio_valido'
                    ) THEN
                        ALTER TABLE vehiculos ADD CONSTRAINT chk_anio_valido 
                        CHECK (anio >= 1900 AND anio <= EXTRACT(YEAR FROM CURRENT_DATE) + 1);
                    END IF;
                END$$;
            """))

            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'chk_precio_positivo'
                    ) THEN
                        ALTER TABLE vehiculos ADD CONSTRAINT chk_precio_positivo 
                        CHECK (precio > 0);
                    END IF;
                END$$;
            """))

            conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'chk_email_valido'
                    ) THEN
                        ALTER TABLE usuarios ADD CONSTRAINT chk_email_valido 
                        CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');
                    END IF;
                END$$;
            """))

    except Exception as e:
        logger.error(f"Error creating views: {str(e)}")
        raise
