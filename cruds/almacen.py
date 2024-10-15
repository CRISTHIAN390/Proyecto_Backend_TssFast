import os
from fastapi import HTTPException
from database import create_connection
from models.almacen import AlmacenCreate
import mysql.connector

def create_almacen(almacn: AlmacenCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO almacen(nombre_almacen,ubicacion_almacen,descripcion_almacen,estado_almacen ) 
                          VALUES (%s,%s,%s,%s)''',
                       (almacn.nombre_almacen,almacn.ubicacion_almacen,almacn.descripcion_almacen,almacn.estado_almacen))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error en la base de datos: {str(err)}")
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "almacen creado con exito"}


def read_almacenes():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                    SELECT * FROM almacen a
                    WHERE a.estado_almacen = 1;
                   """)
    almacenes = cursor.fetchall()
    conn.close()
    return almacenes


def select_almacenid(idalmacen: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM almacen WHERE idalmacen = %s", (idalmacen,))
    almacen = cursor.fetchone()
    conn.close()

    if almacen is None:
        raise HTTPException(status_code=404, detail="almacen no encontrada")
    return almacen


def update_almacen(idalmacen: int, alma: AlmacenCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE almacen SET nombre_almacen = %s, ubicacion_almacen = %s, descripcion_almacen = %s, estado_almacen = %s
                          WHERE idalmacen = %s''',
                       (alma.nombre_almacen, alma.ubicacion_almacen, alma.descripcion_almacen, alma.estado_almacen, idalmacen))
        conn.commit()  # Confirmar los cambios en la base de datos
    except mysql.connector.Error as err:
        conn.rollback()  # Revertir cambios en caso de error
        raise HTTPException(status_code=400, detail=str(err))  # Lanzar una excepción HTTP
    finally:
        conn.close()  # Asegurarse de cerrar la conexión

    return {"message": "almacen actualizado actualizado con éxito"}


def delete_almacen(idalmacn: int):
    #corrigue el que envio es idcliente
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    try:
        # Actualiza el estado del idalmacen de 1 a 0 (desactivado)
        cursor.execute('''UPDATE almacen SET estado_almacen = 0
                          WHERE idalmacen = %s
                        
                        ''', (idalmacn,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "El almacen se eliminó con éxito"}
