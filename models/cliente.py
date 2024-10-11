from pydantic import BaseModel

class ClienteCreate(BaseModel):
    apellidos: str
    nombres: str
    dni: str
    celular: str
    preferencias: str
    estado: bool
    