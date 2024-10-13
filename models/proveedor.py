from pydantic import BaseModel

class ProveedorCreate(BaseModel):
    apellidos: str
    nombres: str
    dni: str
    celular: str
    nombre_proveedor:str
    ruc:str
    estado:bool
    