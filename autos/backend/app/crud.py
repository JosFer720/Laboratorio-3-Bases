from sqlalchemy.orm import Session
from app import models, schemas

def crear_vehiculo(db: Session, vehiculo: schemas.VehiculoCreate):
    db_vehiculo = models.Vehiculo(**vehiculo.dict(exclude={"categorias"}))
    if vehiculo.categorias:
        db_vehiculo.categorias = db.query(models.Categoria).filter(models.Categoria.id.in_(vehiculo.categorias)).all()
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

def obtener_vehiculos(db: Session):
    return db.query(models.Vehiculo).all()
