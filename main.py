import os
from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware  # Importa el middleware de CORS
from pydantic import BaseModel
from models.user import UserCreate
from cruds import users, role
from database import  create_database, create_tables_and_insert_data,create_connection
app = FastAPI()

@app.get("/users/count")
def get_user_count():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(f"Error fetching user count: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user count")
    finally:
        cursor.close()
        conn.close()

@app.get("/vigilantes/count")
def get_vigilante_count():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'vigilante')")
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
    allow_origins=["*"],  # Permite todas las orígenes. Cambia esto a un dominio específico en producción.
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
    return users.login_users(login_data.email, login_data.password)



# Crear un nuevo usuario
@app.post("/api/users/")
def create_user(user: UserCreate):
    return users.create_user(user)

# Usuarios
# Listar todos los users
@app.get("/api/users/")
def read_users():
    return users.read_users()

#listar usuario por rol
@app.get("/api/users/role/{user_id}")
def read_usersByRole(user_id: int):
    return users.read_usersByIdRole(user_id)

# Obtener un user por su ID
@app.get("/api/users/{user_id}")
def select_user_by_id(user_id: int):
    return users.select_user_by_id(user_id)

# Actualizar un user
@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    return users.update_user(user_id, user)

@app.put("/api/users/Password/{user_id}")
def update_user(user_id: int, user: UserCreate):
    return users.update_user2(user_id, user)

# Eliminar un user
@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    return users.delete_user(user_id)






# ROLES
# Listar todos los roles
@app.get("/roles/")
def list_roles():
    return role.list_roles()

# Obtener un rol por su ID
@app.get("/roles/{role_id}")
def get_role(role_id: int):
    return role.get_role(role_id)

# Crear un nuevo rol
@app.post("/roles/")
def create_role(role: UserCreate):
    return role.create_role(role)

# Actualizar un rol
@app.put("/roles/{role_id}")
def update_role(role_id: int, role: UserCreate):
    return role.update_role(role_id, role)

# Eliminar un rol
@app.delete("/roles/{role_id}")
def delete_role(role_id: int):
    return role.delete_role(role_id)


class ImagenCapturada(BaseModel):
    frame: str  # Se espera un string que representa el frame

@app.post("/extract_plate/")
async def extraer_data(frame_data: ImagenCapturada):
    return {"success": True, "plate": users.Extraer_Data(frame_data.frame)}


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