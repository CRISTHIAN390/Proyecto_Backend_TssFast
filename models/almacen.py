from pydantic import BaseModel

class AlmacenCreate(BaseModel):
    nombre_almacen: str
    ubicacion_almacen: str
    descripcion_almacen: str
    estado_almacen:int
    

            
     