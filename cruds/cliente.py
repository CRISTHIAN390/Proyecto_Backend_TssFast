import os
from fastapi import HTTPException
from database import create_connection
from models.persona import PersonaCreate
from models.cliente import ClienteCreate
import mysql.connector
from cruds import persona


def create_cliente(client: ClienteCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
     # Creación de la persona
    
    person_data  = PersonaCreate(apellidos=client.apellidos, nombres=client.nombres, dni=client.dni, celular=client.celular, estado=client.estado)
    persona.create_persona(person_data)   
    # Seleccionar idpersona por dni y convertir a entero
    idperson = idperson = int(persona.select_persona_dni(client.dni))
    try:
        cursor.execute('''INSERT INTO cliente (idpersona, preferencias) 
                          VALUES (%s, %s)''',
                       (idperson, client.preferencias))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        conn.close()
    return {"message": "Cliente creado con exito"}


def read_clientes():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                    SELECT
                        c.idcliente,
                        p.apellidos,
                        p.nombres,
                        p.dni,
                        p.celular,
                        c.preferencias,
                        p.estado
                    FROM 
                        cliente c
                    JOIN
                        persona p on c.idpersona=p.idpersona;
                   """)
    clientes = cursor.fetchall()
    conn.close()
    return clientes



def update_cliente(idcliente: int, clien: ClienteCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    
    # Actualiza de la persona
    person_data  = PersonaCreate(apellidos=clien.apellidos, nombres=clien.nombres, dni=clien.dni, celular=clien.celular, estado=1)
    iddata=persona.select_persona_dni(dni=person_data.dni)
    persona.update_persona(idpersona=iddata,PersonaCreate=person_data)
    try:
        cursor.execute('''UPDATE cliente SET preferencias = %s
                          WHERE idcliente = %s''',
                       (clien.preferencias,idcliente))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        conn.close()
    return {"message": "Cliente actualizado con exito"}
