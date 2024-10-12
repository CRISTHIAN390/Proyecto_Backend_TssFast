from pydantic import BaseModel

class PersonaCreat(BaseModel):
    apellidos: str
    nombres: str
    dni: str
    celular: str
    estado:bool
    