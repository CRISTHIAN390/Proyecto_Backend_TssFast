from pydantic import BaseModel
from typing import Optional
class ProductoCreate(BaseModel):
    idtipo: int
    nombre_producto: str
    stock_producto: int
    unidad_de_medida: str
    precio_producto: float
    