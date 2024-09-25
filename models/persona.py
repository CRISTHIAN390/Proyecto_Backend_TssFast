from pydantic import BaseModel

class PersonaCreate(BaseModel):
    apellidos: str
    nombres: str
    dni: str
    celular: str
    estado:int
    