import os
from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware  # Importa el middleware de CORS
from pydantic import BaseModel
from models.usuario import UsuarioCreate,UsuarioCrear,UsuarioAcceso
from models.cliente import ClienteCreate
from models.proveedor import ProveedorCreate
from models.almacen import AlmacenCreate
 
from models.rol import RolCreate
from cruds import usuario, rol,cliente,proveedor,almacen
from database import  create_database, create_tables_and_insert_data,create_connection
app = FastAPI()


@app.get("/usuarios/count")
def get_user_count():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM usuario")
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(f"Error fetching user count: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user count")
    finally:
        cursor.close()
        conn.close()


@app.get("/transportista/count")
def get_vigilante_count():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE role_id = (SELECT idrol FROM rol WHERE nombre_rol = 'transportista')")
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(f"Error fetching vigilante count: {e}")
        raise HTTPException(status_code=500, detail="Error fetching vigilante count")
    finally:
        cursor.close()
        conn.close()


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],# Permite todas las orígenes. Cambia esto a un dominio específico en producción.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.).
    allow_headers=["*"],  # Permite todos los encabezados.
)


# Inicializar la base de datos al arrancar la aplicación utilizando el nuevo esquema Lifespan
@app.on_event("startup")
async def startup_event():
    create_database()
    create_tables_and_insert_data()


# Ruta raíz para verificar que la API está funcionando
@app.get("/")
def read_root():
    return {"message": "La API está en funcionamiento!"}


# Iniciar sesión de usuario
class LoginData(BaseModel):
    email: str
    password: str
@app.post("/login/")
def login(login_data: LoginData):
    return usuario.login_users(login_data.email, login_data.password)


# Usuarios
# Crear un nuevo usuario
@app.post("/api/usuario/")
def crear_usuario(perso: UsuarioCrear):
    return usuario.create_usuario(perso)


# Listar todos los users
@app.get("/api/usuario/")
def listar_usuarios():
    return usuario.read_usuarios()


#listar usuarios por rol
@app.get("/api/usuario/rol/{idrol}")
def leer_usuarioByRol(idrol: int):
    return usuario.read_usuarioByIdRol(idrol)


# Obtener un user por su ID
@app.get("/api/usuario/{idusuario}")
def selectByusuario(idusuario: int):
    return usuario.select_usuario_by_id(idusuario)


# Actualizar un user
@app.put("/api/usuario/{idusuario}")
def actualizar_usuario(idusuario: int, user: UsuarioCreate):
    return usuario.update_usuario(idusuario, user,False)


# Actualizar clave de un usuario
@app.put("/api/usuario/password/{idusuario}")
def actualizar_clave(idusuario: int, user: UsuarioCreate):
    return usuario.update_usuario(idusuario, user,True)


# Actualizar un acceso rol-estado
@app.put("/api/usuario/acceso/{idusuario}")
def actualizar_acceso(idusuario: int, useracc: UsuarioAcceso):
    return usuario.update_acceso(idusuario, useracc)


# Eliminar un user
@app.delete("/api/usuario/{idusuario}")
def eliminar_usuario(idusuario: int):
    return usuario.delete_usuario(idusuario)


# ROLES
# Listar todos los roles
@app.get("/api/rol/")
def listar_roles():
    return rol.list_roles()


# Obtener un rol por su ID
@app.get("/api/rol/{idrol}")
def get_rol(idrol: int):
    return rol.get_rol(idrol)


# Crear un nuevo rol
@app.post("/api/rol/")
def crear_rol(roll: RolCreate):
    return rol.create_role(roll)


# Actualizar un rol
@app.put("/api/rol/{idrol}")
def actualizar_rol(idrol: int, roll: RolCreate):
    return rol.update_role(idrol, roll)


# Eliminar un rol
@app.delete("/api/rol/{idrol}")
def eliminar_rol(idrol: int):
    return rol.delete_rol(idrol)


#Añadir mas campos
# Listar todos los clientes
@app.get("/api/cliente/")
def listar_clientes():
    return cliente.read_clientes()

@app.post("/api/cliente/")
def create_cliente(clien: ClienteCreate):
    return cliente.create_cliente(clien)

# Obtener un cliente por su ID
@app.put("/api/cliente/{idcliente}")
def update_cliente(idcliente: int, clien: ClienteCreate):
    
    return cliente.update_cliente(idcliente, clien)

# Eliminar un cliente
@app.delete("/api/cliente/{idcliente}")
def delete_cliente(idcliente: int):
    return cliente.delete_cliente(idcliente)

# Listar todos los proveedor
@app.get("/api/proveedor/")
def listar_proveedores():
    return proveedor.read_proveedores()

# crear proveedor
@app.post("/api/proveedor/")
def create_proveedor(prove: ProveedorCreate):
    return proveedor.create_proveedor(prove)

# Obtener un cliente por su ID
@app.put("/api/proveedor/{idproveedor}")
def update_proveedor(idproveedor: int, prove: ProveedorCreate):
    return proveedor.update_proveedor(idproveedor, prove)

# Eliminar un proveedor
@app.delete("/api/proveedor/{idproveedor}")
def delete_proveedor(idproveedor: int):
    return proveedor.delete_proveedor(idproveedor)


# Listar todos los almacen
@app.get("/api/almacen/")
def listar_almacenes():
    return almacen.read_almacenes()

# crear almacen
@app.post("/api/almacen/")
def create_almacen(alma: AlmacenCreate):
    return almacen.create_almacen(alma)

# Obtener un almacen por su ID
@app.put("/api/almacen/{idalmacen}")
def update_almacen(idalmacen: int, alma: AlmacenCreate):
    return almacen.update_almacen(idalmacen, alma)

# Eliminar un almacen
@app.delete("/api/almacen/{idalmacen}")
def delete_almacen(idalmacen: int):
    return almacen.delete_almacen(idalmacen)


#SECCION ABASTECIMIENTO

















# Listar todos los vehiculo
#    @app.get("/api/vehiculo/")
#    def listar_vehiculos():
#        return almacen.read_vehiculos()



#Para el modulo de vehiculo
class ImagenCapturada(BaseModel):
    frame: str  # Se espera un string que representa el frame
@app.post("/extract_plate/")
async def extraer_data(frame_data: ImagenCapturada):
    return {"success": True, "plate": usuario.Extraer_Data(frame_data.frame)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
      #  "main:app",
        host="127.0.0.1",
        port=4500,
        reload=True,  #Equivale a un debug
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )
#Para ejecutar el proyecto :uvicorn main:app --reload --port 4500 --host 127.0.0.1 