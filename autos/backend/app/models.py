from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, DECIMAL, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

vehiculo_categoria = Table(
    'vehiculo_categoria', Base.metadata,
    Column('vehiculo_id', Integer, ForeignKey('vehiculos.id', ondelete='CASCADE'), primary_key=True),
    Column('categoria_id', Integer, ForeignKey('categorias.id'), primary_key=True)
)

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena = Column(Text, nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Marca(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    marca_id = Column(Integer, ForeignKey("marcas.id"), nullable=False)
    modelo = Column(String(100), nullable=False)
    anio = Column(Integer, nullable=False)
    tipo = Column(String(50))
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    disponible = Column(Boolean, default=True)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)
    categorias = relationship("Categoria", secondary=vehiculo_categoria, back_populates="vehiculos")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    vehiculos = relationship("Vehiculo", secondary=vehiculo_categoria, back_populates="categorias")
