from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from app.database import engine
from app import models
import logging
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

def create_tables():
    logger.info("Creando tablas...")
    models.Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas exitosamente")

def insert_initial_data():
    with Session(bind=engine) as db:
        try:
            if not db.scalars(select(models.Rol)).first():
                roles = ['admin', 'vendedor', 'cliente']
                logger.info(f"Insertando {len(roles)} roles")
                db.add_all([models.Rol(nombre=nombre) for nombre in roles])
                db.commit()
            
            if not db.scalars(select(models.Usuario)).first():
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
                db.add_all([
                    models.Usuario(
                        nombre=u[0],
                        email=u[1],
                        contrasena=u[2],
                        rol_id=u[3],
                        fecha_creacion=datetime.utcnow()
                    ) for u in usuarios
                ])
                db.commit()
            
            if not db.scalars(select(models.Marca)).first():
                marcas = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan', 
                          'BMW', 'Audi', 'Hyundai', 'Kia', 'Mazda']
                logger.info(f"Insertando {len(marcas)} marcas")
                db.add_all([models.Marca(nombre=nombre) for nombre in marcas])
                db.commit()
            
            if not db.scalars(select(models.Categoria)).first():
                categorias = ['Económico', 'Deportivo', 'SUV', 'Pickup', 'Familiar',
                              'Compacto', 'Convertible', 'Lujo', 'Híbrido', 'Eléctrico']
                logger.info(f"Insertando {len(categorias)} categorías")
                db.add_all([models.Categoria(nombre=nombre) for nombre in categorias])
                db.commit()
            
            if not db.scalars(select(models.Vehiculo)).first():
                vehiculos = [
                    (1, 'Corolla', 2020, 'Sedán', 'Confiable y económico', Decimal("15500.00"), 6),
                    (1, 'Camry', 2021, 'Sedán', 'Amplio y seguro', Decimal("22000.00"), 7),
                    (2, 'Civic', 2019, 'Sedán', 'Deportivo y eficiente', Decimal("18000.00"), 8),
                    (2, 'CR-V', 2022, 'SUV', 'Espacioso con buena tecnología', Decimal("28000.00"), 9),
                    (3, 'Focus', 2018, 'Hatchback', 'Compacto ideal para ciudad', Decimal("12000.00"), 10),
                    (3, 'F-150', 2023, 'Pickup', 'Potente y resistente', Decimal("35000.00"), 6),
                    (4, 'Malibu', 2020, 'Sedán', 'Elegante con buen consumo', Decimal("19000.00"), 7),
                    (4, 'Tahoe', 2021, 'SUV', 'Ideal para familias grandes', Decimal("45000.00"), 8),
                    (5, 'Altima', 2019, 'Sedán', 'Estilo moderno y rendimiento sólido', Decimal("17000.00"), 9),
                    (5, 'Frontier', 2022, 'Pickup', 'Trabajo pesado', Decimal("31000.00"), 10),
                    (6, 'Serie 3', 2021, 'Sedán', 'Lujo y precisión alemana', Decimal("38000.00"), 6),
                    (6, 'X5', 2023, 'SUV', 'Potencia y espacio', Decimal("60000.00"), 7),
                    (7, 'A4', 2020, 'Sedán', 'Elegancia y tecnología', Decimal("35000.00"), 8),
                    (7, 'Q7', 2022, 'SUV', 'Lujoso para familias', Decimal("65000.00"), 9),
                    (8, 'Elantra', 2021, 'Sedán', 'Eficiencia y conectividad', Decimal("16000.00"), 10),
                    (8, 'Tucson', 2022, 'SUV', 'Diseño y seguridad', Decimal("25000.00"), 6),
                    (9, 'Rio', 2019, 'Compacto', 'Ideal para principiantes', Decimal("11000.00"), 7),
                    (9, 'Sportage', 2023, 'SUV', 'Versatilidad total', Decimal("27000.00"), 8),
                    (10, 'Mazda3', 2020, 'Sedán', 'Estética y manejo', Decimal("17500.00"), 9),
                    (10, 'CX-5', 2021, 'SUV', 'Elegancia japonesa', Decimal("29000.00"), 10),
                    (1, 'Prius', 2022, 'Híbrido', 'Híbrido clásico', Decimal("23000.00"), 6),
                    (2, 'Insight', 2021, 'Híbrido', 'Híbrido elegante', Decimal("24000.00"), 7),
                    (3, 'Mustang', 2022, 'Deportivo', 'Potencia y estilo', Decimal("42000.00"), 8),
                    (4, 'Bolt EV', 2023, 'Eléctrico', '100% eléctrico', Decimal("37000.00"), 9),
                    (5, 'Leaf', 2020, 'Eléctrico', 'Accesible y ecológico', Decimal("19000.00"), 10),
                    (6, 'i3', 2019, 'Eléctrico', 'Diseño futurista', Decimal("33000.00"), 6),
                    (7, 'e-tron', 2021, 'Eléctrico', 'SUV eléctrico premium', Decimal("55000.00"), 7),
                    (8, 'Ioniq', 2020, 'Híbrido', 'Excelente autonomía', Decimal("21000.00"), 8),
                    (9, 'Niro', 2021, 'Híbrido', 'Práctico y eficiente', Decimal("22000.00"), 9),
                    (10, 'MX-30', 2022, 'Eléctrico', 'Compacto ecológico', Decimal("28000.00"), 10)
                ]
                logger.info(f"Insertando {len(vehiculos)} vehículos")
                db.add_all([
                    models.Vehiculo(
                        marca_id=v[0],
                        modelo=v[1],
                        anio=v[2],
                        tipo=v[3],
                        descripcion=v[4],
                        precio=v[5],
                        vendedor_id=v[6],
                        fecha_publicacion=datetime.utcnow()
                    ) for v in vehiculos
                ])
                db.commit()
            
            if not db.execute(select(models.vehiculo_categoria)).first():
                relaciones = [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 6), (6, 4), (7, 1), (8, 3), (9, 1), (10, 4),
                    (11, 8), (12, 3), (13, 8), (14, 3), (15, 1), (16, 3), (17, 6), (18, 3), (19, 1), (20, 3),
                    (21, 9), (22, 9), (23, 2), (24, 10), (25, 10), (26, 10), (27, 10), (28, 9), (29, 9), (30, 10)
                ]
                logger.info(f"🔗 Insertando {len(relaciones)} relaciones vehículo-categoría")
                db.execute(
                    insert(models.vehiculo_categoria),
                    [{"vehiculo_id": vc[0], "categoria_id": vc[1]} for vc in relaciones]
                )
                db.commit()

            logger.info("Datos iniciales insertados exitosamente")

        except Exception as e:
            db.rollback()
            logger.error(f"Error insertando datos: {str(e)}")
            raise
