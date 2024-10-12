import os
from fastapi import HTTPException
from database import create_connection
from models.persona import PersonaCreat
import mysql.connector

def create_persona(person: PersonaCreat):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO persona (apellidos, nombres, dni, celular,estado) 
                          VALUES (%s, %s, %s, %s, %s)''',
                       (person.apellidos, person.nombres, person.dni, person.celular, person.estado))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Persona creado con exito"}


def read_personas():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM persona")
    personas = cursor.fetchall()
    conn.close()
    return personas

def select_persona_dni(dni: str):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM persona WHERE dni = %s", (dni,))
    person = cursor.fetchone()
    conn.close()

    if person is None:
        raise HTTPException(status_code=404, detail="persona no encontrada")
    return person["idpersona"]

def select_persona_by_id(idpersona: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM persona WHERE idpersona = %s", (idpersona,))
    person = cursor.fetchone()
    conn.close()

    if person is None:
        raise HTTPException(status_code=404, detail="persona no encontrada")
    return person

def update_persona(idpersona: int, person: PersonaCreat):
    conn = create_connection()  # Asegúrate de que esta función se define correctamente
    conn.database = os.getenv("DB_NAME")  # Verifica que la variable de entorno esté bien configurada
    cursor = conn.cursor()
    
    try:
        cursor.execute('''UPDATE persona SET apellidos = %s, nombres = %s, dni = %s, celular = %s, estado = %s
                          WHERE idpersona = %s''',
                       (person.apellidos, person.nombres, person.dni, person.celular, person.estado, idpersona))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))  # Lanza excepción HTTP en caso de error
    finally:
        cursor.close()  # Cierra el cursor
    return {"message": "Persona actualizada con éxito"}

def delete_persona(idpersona: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        # Actualiza el estado del usuario de 1 a 0
        cursor.execute("UPDATE persona SET state = 0 WHERE idpersona = %s", (idpersona,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        conn.close()

    return {"message": "Persona eliminada con exito"}