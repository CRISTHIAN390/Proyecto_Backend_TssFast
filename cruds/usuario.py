import os
from fastapi import HTTPException
from database import create_connection
import bcrypt
from models.usuario import UsuarioCreate,UsuarioCrear,UsuarioAcceso
from models.persona import PersonaCreat
import mysql.connector
from cruds import persona

def create_usuario(user: UsuarioCrear):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    
    # Creación de la persona
    person_data  = PersonaCreat(apellidos=user.apellidos, nombres=user.nombres, dni=user.dni, celular="000000000", estado=1)
    persona.create_persona(person_data)
    
    # Seleccionar idpersona por dni y convertir a entero
    idperson = int(persona.select_persona_dni(str(user.dni)))
    
    # Aquí eliminamos la coma para evitar la creación de una tupla
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode()
    try:
        cursor.execute('''INSERT INTO usuario (email, password, idrol, idpersona, fechacreacion, estado) 
                          VALUES (%s, %s, %s, %s, NOW(), %s)''',
                       (user.email, hashed_password, user.idrol, idperson, user.estado))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Usuario creado con éxito"}

# Función para leer todos los usuarios
def read_usuarios():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)
#SELECT * FROM usuario
    cursor.execute("""
                    SELECT 
                        u.idusuario,
                        p.apellidos,
                        p.nombres,
                        u.email,
                        r.idrol,
                        r.nombre_rol,
                        p.dni,
                        u.estado
                    FROM 
                        Usuario u
                    JOIN 
                        Persona p ON u.idpersona = p.idpersona
                    JOIN 
                        Rol r ON u.idrol = r.idrol
                    WHERE 
                        u.idusuario <> 1;
                    """)
    usuarios = cursor.fetchall()
    conn.close()

    return usuarios
# Función para leer usuarios por ID de rol
def read_usuarioByIdRol(idrol: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuario WHERE idrol = %s", (idrol,))
    usuarios = cursor.fetchall()
    conn.close()

    return usuarios

# Función para seleccionar usuario por ID
def select_usuario_by_id(idusuario: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuario WHERE idusuario = %s", (idusuario,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

# Función para actualizar usuario (incluyendo opción para encriptar la clave si es necesaria)
def update_usuario(idusuario: int, usuario: UsuarioCreate, update_password: bool):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        # Si se debe actualizar la contraseña, la encriptamos
        if update_password:
            hashed_password = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt()).decode()
        else:
            # Si no, mantenemos la contraseña original (sin modificarla)
            hashed_password = usuario.password

        cursor.execute('''UPDATE usuario SET email = %s, password = %s, idrol = %s, idpersona = %s, estado = %s
                          WHERE idusuario = %s''',
                       (usuario.email, hashed_password, usuario.idrol, usuario.idpersona, usuario.estado, idusuario))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Usuario actualizado con éxito"}

def update_acceso(idusuario: int, userr: UsuarioAcceso):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE usuario SET idrol = %s, estado = %s
                          WHERE idusuario = %s''',
                       (userr.idrol, userr.estado, idusuario))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Usuario actualizado con éxito"}    
    
# Función para eliminar (desactivar) un usuario
def delete_usuario(idusuario: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        # Actualiza el estado del usuario de 1 a 0 (desactivado)
        cursor.execute("UPDATE usuario SET estado = 0 WHERE idusuario = %s", (idusuario,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "El usuario se eliminó con éxito"}

def login_users(email: str, password: str):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)
    try:
        # Asegúrate de que el parámetro sea una tupla
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            stored_password = usuario['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                idrol = usuario['idrol']
                #print(idrol)
                # Obtener el nombre del rol
                cursor.execute("SELECT nombre_rol FROM rol WHERE idrol = %s", (idrol,))
                nombre_rol = cursor.fetchone()
                # Devolver los datos del usuario y el nombre del rol
                user_data = {
                    "idusuario": usuario['idusuario'],
                    "email": usuario['email'],
                    "idrol": nombre_rol,
                    "message": "Login exitoso"
                }
                return user_data
            else:
                raise HTTPException(status_code=401, detail="Password incorrecto(Unauthorized)")
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()  
        conn.close()

def Extraer_Data(frame: str):
    try:
        ObtenerFrame = frame
        # Aquí simplemente retornamos "*_*" como prueba.
        plate = "mre"
        return plate
    except Exception as e:
        # En caso de error, puedes imprimir el error o manejarlo según tus necesidades
        print(f"Error procesando el frame: {e}")
        # Puedes devolver un valor por defecto o una señal de error
        return "No se detecto"