import os
from fastapi import FastAPI, UploadFile, File,Form, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware  # Importa el middleware de CORS
from pydantic import BaseModel
from models.usuario import UsuarioCreate,UsuarioCrear,UsuarioAcceso
from models.cliente import ClienteCreate
from models.proveedor import ProveedorCreate
from models.almacen import AlmacenCreate
from models.producto import ProductoCreate
from models.tipo import TipoCreate
from models.rol import RolCreate
from cruds import usuario, rol,cliente,proveedor,almacen,producto,tipo
from database import  create_database, create_tables_and_insert_data,create_connection

#extra
from fastapi.responses import JSONResponse
from typing import Optional
import json
from fastapi.staticfiles import StaticFiles


app = FastAPI()
# Montar la carpeta img para servir archivos estáticos
app.mount("/img", StaticFiles(directory="img"), name="img")

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

# ============================================
# USUARIOS
# ============================================
# Crear un nuevo usuario
@app.post("/api/usuario/")
def create_usuario(perso: UsuarioCrear):
    return usuario.create_usuario(perso)

# Listar todos los users
@app.get("/api/usuario/")
def read_usuarios():
    return usuario.read_usuarios()

#listar usuarios por rol
@app.get("/api/usuario/rol/{idrol}")
def usuarioidrol(idrol: int):
    return usuario.read_usuarioByIdRol(idrol)

# Obtener un user por su ID
@app.get("/api/usuario/{idusuario}")
def select_usuario_by_id(idusuario: int):
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
def update_acceso(idusuario: int, useracc: UsuarioAcceso):
    return usuario.update_acceso(idusuario, useracc)

# Eliminar un user
@app.delete("/api/usuario/{idusuario}")
def delete_usuario(idusuario: int):
    return usuario.delete_usuario(idusuario)

# ============================================
# ROLES
# ============================================
# Listar todos los roles
@app.get("/api/rol/")
def list_roles():
    return rol.list_roles()

# Obtener un rol por su ID
@app.get("/api/rol/{idrol}")
def get_rol(idrol: int):
    return rol.get_rol(idrol)

# Crear un nuevo rol
@app.post("/api/rol/")
def create_role(roll: RolCreate):
    return rol.create_rol(roll)

# Actualizar un rol
@app.put("/api/rol/{idrol}")
def update_rol(idrol: int, roll: RolCreate):
    return rol.update_rol(idrol, roll)

# Eliminar un rol
@app.delete("/api/rol/{idrol}")
def delete_rol(idrol: int):
    return rol.delete_rol(idrol)

# ============================================
# CLIENTES
# ============================================
# Listar todos los clientes
@app.get("/api/cliente/")
def read_clientes():
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

# ============================================
# PROVEEDORES
# ============================================
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

# ============================================
# ALMACEN
# ============================================
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

# ============================================
# PRODUCTOS
# ============================================
# Listar todos los productos
@app.get("/api/producto/")
def list_productos():
    return producto.list_productos()

# Modelo del producto
class ProductoCreate(BaseModel):
    idtipo: int
    nombre_producto: str
    stock_producto: int
    unidad_de_medida: str
    precio_producto: float

# Ruta para crear el producto
@app.post("/api/producto/")
def create_producto(
    idtipo: int = Form(...),
    nombre_producto: str = Form(...),
    stock_producto: int = Form(...),
    unidad_de_medida: str = Form(...),
    precio_producto: float = Form(...),
    file: Optional[UploadFile] = File(None)):
    # Crear la instancia del modelo con los datos del formulario
    print("Data recibida")
    producto_model = ProductoCreate(
        idtipo=idtipo,
        nombre_producto=nombre_producto,
        stock_producto=stock_producto,
        unidad_de_medida=unidad_de_medida,
        precio_producto=precio_producto
    )

    # Llamar al proceso de guardado
    return producto.proceso_guardado(producto_model, file)

# extraer un  producto
@app.get("/api/producto/{idproducto}")
def get_producto(idproducto: int):
    return producto.get_producto(idproducto)

# Editar Producto
@app.put("/api/producto/{idproducto}")
def update_producto(
    idproducto: int,
    idtipo: int = Form(...),
    nombre_producto: str = Form(...),
    stock_producto: int = Form(...),
    unidad_de_medida: str = Form(...),
    precio_producto: float = Form(...),
    file: Optional[UploadFile] = File(None)):
    # Crear el modelo con los datos actualizados
    producto_model = ProductoCreate(
        idtipo=idtipo,
        nombre_producto=nombre_producto,
        stock_producto=stock_producto,
        unidad_de_medida=unidad_de_medida,
        precio_producto=precio_producto
    )
    # Llamar a la función de actualización
    return producto.update_producto(idproducto, producto_model, file)

# Eliminar un  producto
@app.delete("/api/producto/{idproducto}")
def delete_producto(idproducto: int):
    return producto.delete_producto(idproducto)

# ============================================
# TIPOS
# ============================================
# Listar todos los tipos
@app.get("/api/producto/tipo/")
def list_tipos():
    return tipo.list_tipos()

# crear producto
@app.post("/api/producto/tipo/")
def create_tipo(tip: TipoCreate):
    return tipo.create_tipo(tip)

# Obtener un producto por su ID
@app.put("/api/producto/tipo/{idtipo}")
def update_tipo(idtipo: int, tip: TipoCreate):
    return tipo.update_tipo(idtipo,tip)

# Eliminar un  producto
@app.delete("/api/producto/tipo/{idtipo}")
def delete_tipo(idtipo: int):
    return tipo.delete_tipo(idtipo)

# ============================================
# Abastecimiento
# ============================================










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