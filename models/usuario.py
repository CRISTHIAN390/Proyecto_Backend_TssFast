from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    email: str
    password: str
    idrol: int
    idpersona: int
    fechacreacion: str
    estado:int

class UsuarioCrear(BaseModel):
    apellidos:str
    nombres: str
    dni:str
    email: str
    password: str
    idrol: int
    estado:int
    