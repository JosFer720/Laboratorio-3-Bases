from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
import logging

router = APIRouter(prefix="/api/vehiculos", tags=["vehiculos"])

@router.get("/")
async def obtener_vehiculos(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM vista_vehiculos"))
        vehiculos = [dict(row._mapping) for row in result]
        return {"data": vehiculos, "status": "success"}
    except Exception as e:
        logging.error(f"Error al obtener vehículos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))