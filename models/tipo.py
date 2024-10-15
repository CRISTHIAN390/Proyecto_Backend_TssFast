from pydantic import BaseModel

class TipoCreate(BaseModel):
    nombre_tipo: str
    estado_tipo: int
    

            
     