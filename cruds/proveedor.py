import os
from fastapi import HTTPException
from database import create_connection
from models.persona import PersonaCreat
from models.proveedor import ProveedorCreate
import mysql.connector
from cruds import persona

def create_proveedor(prove: ProveedorCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    
     # Creación de la persona
    person_data  = PersonaCreat(apellidos=prove.apellidos, nombres=prove.nombres, dni=prove.dni, celular="000000000", estado=1)
    persona.create_persona(person_data)   
    
    # Seleccionar idpersona por dni y convertir a entero
    idperson = int(persona.select_persona_dni(str(prove.dni)))
       
    try:
        cursor.execute('''INSERT INTO proveedor (idpersona, nombre_proveedor, ruc) 
                          VALUES (%s, %s, %s)''',
                       (idperson, prove.nombre_proveedor, prove.ruc))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        conn.close()

    return {"message": "Proveedor creado con exito"}


def read_proveedores():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                    SELECT
                        c.idproveedor,
                        p.apellidos,
                        p.nombres,
                        p.dni,
                        p.celular,
                        c.nombre_proveedor,
                        c.ruc,
                        p.estado
                    FROM 
                        proveedor c
                    JOIN
                        persona p on c.idpersona=p.idpersona;
                   """)
    provedores = cursor.fetchall()
 
    conn.close()
    return provedores