from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True 

class VehiculoBase(BaseModel):
    marca_id: int
    modelo: str
    anio: int
    tipo: Optional[str]
    descripcion: Optional[str]
    precio: Decimal = Field(..., max_digits=10, decimal_places=2) 
    vendedor_id: int
    disponible: Optional[bool] = True

class VehiculoCreate(VehiculoBase):
    categorias: List[int] = []

class Vehiculo(VehiculoBase):
    id: int
    fecha_publicacion: datetime
    categorias: List[Categoria] = []

    class Config:
        from_attributes = True 

class VehiculoVista(BaseModel):
    id: int
    modelo: str
    anio: int
    precio: Decimal
    tipo: Optional[str]
    descripcion: Optional[str]
    marca: str
    vendedor: str
    disponible: bool
    fecha_publicacion: datetime
    categorias: Optional[str]

    class Config:
        from_attributes = True

class UsuarioPublico(BaseModel):
    id: int
    nombre: str