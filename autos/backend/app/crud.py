from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text
from app import models, schemas
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status

# CREATE
def crear_vehiculo(db: Session, vehiculo: schemas.VehiculoCreate):
    # Validaciones a nivel aplicación
    if vehiculo.anio < 1900 or vehiculo.anio > datetime.now().year + 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El año del vehículo no es válido"
        )
    
    if vehiculo.precio <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio debe ser mayor a 0"
        )
    
    # Verificar existencia de marca y vendedor
    if not db.query(models.Marca).filter(models.Marca.id == vehiculo.marca_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La marca especificada no existe"
        )
    
    if not db.query(models.Usuario).filter(models.Usuario.id == vehiculo.vendedor_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El vendedor especificado no existe"
        )
    
    # Crear vehículo
    db_vehiculo = models.Vehiculo(**vehiculo.dict(exclude={"categorias"}))
    
    # Asociar categorías con validación
    if vehiculo.categorias:
        categorias_existentes = db.query(models.Categoria).filter(
            models.Categoria.id.in_(vehiculo.categorias)
        ).all()
        
        if len(categorias_existentes) != len(vehiculo.categorias):
            ids_existentes = {c.id for c in categorias_existentes}
            ids_no_existentes = [id for id in vehiculo.categorias if id not in ids_existentes]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Las siguientes categorías no existen: {ids_no_existentes}"
            )
        
        db_vehiculo.categorias = categorias_existentes
    
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

# READ (Todos los vehículos)
def obtener_vehiculos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehiculo).offset(skip).limit(limit).all()

# READ (Vehículo por ID)
def obtener_vehiculo(db: Session, vehiculo_id: int):
    vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    return vehiculo

# UPDATE
def actualizar_vehiculo(
    db: Session, 
    vehiculo_id: int, 
    vehiculo: schemas.VehiculoCreate
):
    db_vehiculo = obtener_vehiculo(db, vehiculo_id)
    
    # Validar marca si se actualiza
    if vehiculo.marca_id != db_vehiculo.marca_id:
        if not db.query(models.Marca).filter(models.Marca.id == vehiculo.marca_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La nueva marca especificada no existe"
            )
    
    # Validar vendedor si se actualiza
    if vehiculo.vendedor_id != db_vehiculo.vendedor_id:
        if not db.query(models.Usuario).filter(models.Usuario.id == vehiculo.vendedor_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El nuevo vendedor especificado no existe"
            )
    
    # Actualizar campos simples
    for key, value in vehiculo.dict(exclude={"categorias"}).items():
        setattr(db_vehiculo, key, value)
    
    # Actualizar categorías si se proporcionan
    if vehiculo.categorias is not None:
        categorias_existentes = db.query(models.Categoria).filter(
            models.Categoria.id.in_(vehiculo.categorias)
        ).all()
        
        if len(categorias_existentes) != len(vehiculo.categorias):
            ids_existentes = {c.id for c in categorias_existentes}
            ids_no_existentes = [id for id in vehiculo.categorias if id not in ids_existentes]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Las siguientes categorías no existen: {ids_no_existentes}"
            )
        
        db_vehiculo.categorias = categorias_existentes
    
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

# DELETE
def eliminar_vehiculo(db: Session, vehiculo_id: int):
    db_vehiculo = obtener_vehiculo(db, vehiculo_id)
    db.delete(db_vehiculo)
    db.commit()
    return {"ok": True}

# Funciones adicionales para relaciones
def agregar_categoria_a_vehiculo(db: Session, vehiculo_id: int, categoria_id: int):
    vehiculo = obtener_vehiculo(db, vehiculo_id)
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    if categoria in vehiculo.categorias:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El vehículo ya tiene esta categoría"
        )
    
    vehiculo.categorias.append(categoria)
    db.commit()
    return vehiculo

def remover_categoria_de_vehiculo(db: Session, vehiculo_id: int, categoria_id: int):
    vehiculo = obtener_vehiculo(db, vehiculo_id)
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    if categoria not in vehiculo.categorias:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El vehículo no tiene esta categoría"
        )
    
    vehiculo.categorias.remove(categoria)
    db.commit()
    return vehiculo

# Función actualizada para obtener vehículos desde la vista SQL
def obtener_vehiculos_desde_vista(db: Session, skip: int = 0, limit: int = 100):
    # Usamos text() para ejecutar SQL directo y mapeamos al schema VehiculoVista
    query = text("""
        SELECT * FROM vista_vehiculos
        ORDER BY id
        OFFSET :skip LIMIT :limit
    """)
    
    result = db.execute(query, {"skip": skip, "limit": limit})
    
    # Mapeamos los resultados al schema Pydantic
    vehiculos = []
    for row in result:
        vehiculos.append(schemas.VehiculoVista(
            id=row.id,
            modelo=row.modelo,
            anio=row.anio,
            precio=row.precio,
            tipo=row.tipo,
            descripcion=row.descripcion,
            marca=row.marca,
            vendedor=row.vendedor,
            disponible=row.disponible,
            fecha_publicacion=row.fecha_publicacion,
            categorias=row.categorias
        ))
    
    return vehiculos