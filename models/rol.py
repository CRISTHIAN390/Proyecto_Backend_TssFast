from pydantic import BaseModel

class RolCreate(BaseModel):
    nombre_rol: str
    estado_rol:int