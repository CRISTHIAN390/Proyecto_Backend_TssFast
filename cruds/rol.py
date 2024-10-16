import os
from fastapi import HTTPException
import mysql.connector
from database import create_connection
from models.rol import RolCreate

# Crear un nuevo rol
def create_rol(rol: RolCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO rol (nombre_rol, estado_rol) VALUES (%s, %s)''', (rol.nombre_rol, rol.estado_rol))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Rol creado con éxito"}

# Listar todos los roles
def list_roles():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
                   SELECT
                        * FROM  rol WHERE idrol!=1;
                   ''')
    roles = cursor.fetchall()
    conn.close()
    return roles

# Obtener un rol por su ID
def get_rol(idrol: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rol WHERE idrol = %s", (idrol,))
    rol = cursor.fetchone()
    conn.close()

    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    return rol

# Actualizar un rol por su ID
def update_rol(idrol: int, rol: RolCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''UPDATE rol SET nombre_rol = %s, estado_rol = %s WHERE idrol = %s''', 
                       (rol.nombre_rol, rol.estado_rol, idrol))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Rol actualizado con éxito"}

# Eliminar (desactivar) un rol por su ID
def delete_rol(idrol: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        # Actualizar el estado del rol a 0 en lugar de eliminarlo
        cursor.execute("UPDATE rol SET estado_rol = %s WHERE idrol = %s", (0, idrol))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Rol eliminado con éxito"}