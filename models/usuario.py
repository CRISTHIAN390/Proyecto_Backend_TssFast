from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    email: str
    password: str
    idrol: int
    idpersona: int
    fechacreacion: str
    estado:int
    