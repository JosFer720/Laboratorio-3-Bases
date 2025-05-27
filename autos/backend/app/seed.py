from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from app.database import engine
from app import models
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_tables():
    """Crea todas las tablas si no existen"""
    logger.info("Verificando tablas...")
    models.Base.metadata.create_all(bind=engine)


def insert_initial_data():
    """Inserta datos iniciales solo si no existen"""
    with Session(bind=engine) as db:
        try:
            if db.scalar(select(models.Rol).limit(1)) is None:
                roles = ['admin', 'vendedor', 'cliente']
                logger.info(f"Insertando {len(roles)} roles")
                for nombre in roles:
                    db.add(models.Rol(nombre=nombre))
                db.commit()
            else:
                logger.info("Roles ya existen, omitiendo inserción")

            if db.scalar(select(models.Usuario).limit(1)) is None:
                usuarios = [
                    ('Admin Uno', 'admin1@mail.com', 'pass123', 1),
                    ('Admin Dos', 'admin2@mail.com', 'pass123', 1),
                    ('Admin Tres', 'admin3@mail.com', 'pass123', 1),
                    ('Admin Cuatro', 'admin4@mail.com', 'pass123', 1),
                    ('Admin Cinco', 'admin5@mail.com', 'pass123', 1),
                    ('Vendedor Uno', 'vend1@mail.com', 'vend123', 2),
                    ('Vendedor Dos', 'vend2@mail.com', 'vend123', 2),
                    ('Vendedor Tres', 'vend3@mail.com', 'vend123', 2),
                    ('Vendedor Cuatro', 'vend4@mail.com', 'vend123', 2),
                    ('Vendedor Cinco', 'vend5@mail.com', 'vend123', 2),
                    ('Vendedor Seis', 'vend6@mail.com', 'vend123', 2),
                    ('Vendedor Siete', 'vend7@mail.com', 'vend123', 2),
                    ('Vendedor Ocho', 'vend8@mail.com', 'vend123', 2),
                    ('Vendedor Nueve', 'vend9@mail.com', 'vend123', 2),
                    ('Vendedor Diez', 'vend10@mail.com', 'vend123', 2),
                    *[(f'Cliente {i}', f'cli{i}@mail.com', 'cli123', 3) for i in range(1, 16)]
                ]
                logger.info(f"Insertando {len(usuarios)} usuarios")
                for u in usuarios:
                    db.add(models.Usuario(
                        nombre=u[0],
                        email=u[1],
                        contrasena=u[2],
                        rol_id=u[3]
                    ))
                db.commit()
            else:
                logger.info("Usuarios ya existen, omitiendo inserción")

            if db.scalar(select(models.Marca).limit(1)) is None:
                marcas = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan',
                          'BMW', 'Audi', 'Hyundai', 'Kia', 'Mazda']
                logger.info(f"Insertando {len(marcas)} marcas")
                for nombre in marcas:
                    db.add(models.Marca(nombre=nombre))
                db.commit()
            else:
                logger.info("Marcas ya existen, omitiendo inserción")

            if db.scalar(select(models.Categoria).limit(1)) is None:
                categorias = ['Económico', 'Deportivo', 'SUV', 'Pickup', 'Familiar',
                             'Compacto', 'Convertible', 'Lujo', 'Híbrido', 'Eléctrico']
                logger.info(f"Insertando {len(categorias)} categorías")
                for nombre in categorias:
                    db.add(models.Categoria(nombre=nombre))
                db.commit()
            else:
                logger.info("Categorías ya existen, omitiendo inserción")

            if db.scalar(select(models.Vehiculo).limit(1)) is None:
                vehiculos = [
                    (1, 'Corolla', 2020, 'Sedán', 'Confiable y económico', 15500.00, 6),
                    (1, 'Camry', 2021, 'Sedán', 'Amplio y seguro', 22000.00, 7),
                    (2, 'Civic', 2019, 'Sedán', 'Deportivo y eficiente', 18000.00, 8),
                    (2, 'CR-V', 2022, 'SUV', 'Espacioso con buena tecnología', 28000.00, 9),
                    (3, 'Focus', 2018, 'Hatchback', 'Compacto ideal para ciudad', 12000.00, 10),
                    (3, 'F-150', 2023, 'Pickup', 'Potente y resistente', 35000.00, 6),
                    (4, 'Malibu', 2020, 'Sedán', 'Elegante con buen consumo', 19000.00, 7),
                    (4, 'Tahoe', 2021, 'SUV', 'Ideal para familias grandes', 45000.00, 8),
                    (5, 'Altima', 2019, 'Sedán', 'Estilo moderno y rendimiento sólido', 17000.00, 9),
                    (5, 'Frontier', 2022, 'Pickup', 'Trabajo pesado', 31000.00, 10),
                ]
                logger.info(f"Insertando {len(vehiculos)} vehículos")
                for v in vehiculos:
                    db.add(models.Vehiculo(
                        marca_id=v[0],
                        modelo=v[1],
                        anio=v[2],
                        tipo=v[3],
                        descripcion=v[4],
                        precio=v[5],
                        vendedor_id=v[6]
                    ))
                db.commit()
            else:
                logger.info("Vehículos ya existen, omitiendo inserción")

            if db.scalar(select(models.vehiculo_categoria).limit(1)) is None:
                relaciones = [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 6), (6, 4),
                    (7, 1), (8, 3), (9, 1), (10, 4)
                ]
                logger.info(f"Insertando {len(relaciones)} relaciones vehículo-categoría")
                for rel in relaciones:
                    stmt = insert(models.vehiculo_categoria).values(
                        vehiculo_id=rel[0],
                        categoria_id=rel[1]
                    )
                    db.execute(stmt)
                db.commit()
            else:
                logger.info("Relaciones ya existen, omitiendo inserción")

        except Exception as e:
            db.rollback()
            logger.error(f"Error en inserción de datos: {str(e)}")
            raise


def init_db():
    """Inicializa la base de datos de manera idempotente"""
    create_tables()
    insert_initial_data()


if __name__ == "__main__":
    init_db()
