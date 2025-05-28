from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/api/vehiculos", tags=["vehiculos"])

@router.post("/", response_model=schemas.Vehiculo, status_code=status.HTTP_201_CREATED)
def crear_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    return crud.crear_vehiculo(db, vehiculo)

@router.get("/", response_model=List[schemas.VehiculoVista])
def listar_vehiculos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_vehiculos_desde_vista(db, skip=skip, limit=limit)

@router.get("/{vehiculo_id}", response_model=schemas.Vehiculo)
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    return crud.obtener_vehiculo(db, vehiculo_id)

@router.put("/{vehiculo_id}", response_model=schemas.Vehiculo)
def actualizar_vehiculo(
    vehiculo_id: int, 
    vehiculo: schemas.VehiculoCreate, 
    db: Session = Depends(get_db)
):
    return crud.actualizar_vehiculo(db, vehiculo_id, vehiculo)

@router.delete("/{vehiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    crud.eliminar_vehiculo(db, vehiculo_id)
    return None

@router.post("/{vehiculo_id}/categorias/{categoria_id}", response_model=schemas.Vehiculo)
def agregar_categoria(
    vehiculo_id: int, 
    categoria_id: int, 
    db: Session = Depends(get_db)
):
    return crud.agregar_categoria_a_vehiculo(db, vehiculo_id, categoria_id)

@router.delete("/{vehiculo_id}/categorias/{categoria_id}", response_model=schemas.Vehiculo)
def remover_categoria(
    vehiculo_id: int, 
    categoria_id: int, 
    db: Session = Depends(get_db)
):
    return crud.remover_categoria_de_vehiculo(db, vehiculo_id, categoria_id)