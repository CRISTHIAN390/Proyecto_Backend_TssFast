from pydantic import BaseModel

class ProveedorCreate(BaseModel):
    nombre_proveedor:str
    ruc:str
    apellidos: str
    nombres: str
    dni: str
    celular: str
    estado:int
    