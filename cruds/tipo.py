import os
from fastapi import HTTPException
from database import create_connection
from models.tipo import TipoCreate
import mysql.connector

# Crear un nuevo tipo
def create_tipo(tipo: TipoCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO Tipo (nombre_tipo, estado_tipo) VALUES (%s, %s)''', 
                       (tipo.nombre_tipo, tipo.estado_tipo))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Tipo creado con éxito"}

# Listar todos los tipos
def list_tipos():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''SELECT * FROM Tipo WHERE estado_tipo != 0;''')  # Solo muestra tipos activos
    tipos = cursor.fetchall()
    conn.close()
    return tipos

# Obtener un tipo por su ID
def get_tipo(idtipo: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Tipo WHERE idtipo = %s", (idtipo,))
    tipo = cursor.fetchone()
    conn.close()

    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")

    return tipo

# Actualizar un tipo por su ID
def update_tipo(idtipo: int, tipo: TipoCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''UPDATE Tipo SET nombre_tipo = %s, estado_tipo = %s WHERE idtipo = %s''', 
                       (tipo.nombre_tipo, tipo.estado_tipo, idtipo))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Tipo actualizado con éxito"}

# Eliminar (desactivar) un tipo por su ID
def delete_tipo(idtipo: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''UPDATE Tipo SET estado_tipo = 0 WHERE idtipo = %s''', (idtipo,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Tipo desactivado con éxito"}
