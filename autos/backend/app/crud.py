from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text
from app import models, schemas
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status

def crear_vehiculo(db: Session, vehiculo: schemas.VehiculoCreate):
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
    
    db_vehiculo = models.Vehiculo(**vehiculo.dict(exclude={"categorias"}))
    
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

def obtener_vehiculos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehiculo).offset(skip).limit(limit).all()

def obtener_vehiculo(db: Session, vehiculo_id: int):
    vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    return vehiculo

def actualizar_vehiculo(
    db: Session, 
    vehiculo_id: int, 
    vehiculo: schemas.VehiculoCreate
):
    db_vehiculo = obtener_vehiculo(db, vehiculo_id)
    
    if vehiculo.marca_id != db_vehiculo.marca_id:
        if not db.query(models.Marca).filter(models.Marca.id == vehiculo.marca_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La nueva marca especificada no existe"
            )
    
    if vehiculo.vendedor_id != db_vehiculo.vendedor_id:
        if not db.query(models.Usuario).filter(models.Usuario.id == vehiculo.vendedor_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El nuevo vendedor especificado no existe"
            )
    
    for key, value in vehiculo.dict(exclude={"categorias"}).items():
        setattr(db_vehiculo, key, value)
    
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

def eliminar_vehiculo(db: Session, vehiculo_id: int):
    db_vehiculo = obtener_vehiculo(db, vehiculo_id)
    db.delete(db_vehiculo)
    db.commit()
    return {"ok": True}

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

def obtener_vehiculos_desde_vista(db: Session, skip: int = 0, limit: int = 100):
    stmt = text("SELECT * FROM vista_vehiculos ORDER BY id OFFSET :skip LIMIT :limit")
    result = db.execute(stmt, {"skip": skip, "limit": limit})
    return [dict(row) for row in result.mappings()]