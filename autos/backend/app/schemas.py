from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        orm_mode = True

class VehiculoBase(BaseModel):
    marca_id: int
    modelo: str
    anio: int
    tipo: Optional[str]
    descripcion: Optional[str]
    precio: float = Field(max_digits=10, decimal_places=2)
    vendedor_id: int
    disponible: Optional[bool] = True

class VehiculoCreate(VehiculoBase):
    categorias: List[int] = []

class Vehiculo(VehiculoBase):
    id: int
    fecha_publicacion: datetime
    categorias: List[Categoria] = []

    class Config:
        orm_mode = True