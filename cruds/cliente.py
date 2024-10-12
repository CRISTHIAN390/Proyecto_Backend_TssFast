import os
from fastapi import HTTPException
from database import create_connection
from models.persona import PersonaCreat
from models.cliente import ClienteCreate
import mysql.connector
from cruds import persona


def create_cliente(client: ClienteCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
     # Creación de la persona
    
    person_data  = PersonaCreat(apellidos=client.apellidos, nombres=client.nombres, dni=client.dni, celular=client.celular, estado=client.estado)
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
        print(f"Error en la base de datos: {str(err)}")
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
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
    
    person_dt = PersonaCreat(
    apellidos=clien.apellidos, 
    nombres=clien.nombres,    
    dni=clien.dni,              
    celular=clien.celular,     
    estado=1                   
    )
    idper =int(select_personaidcliente(idcliente=idcliente))  # Obtener el idpersona del cliente en la base de datos
    
    print(idper) 
    # Actualiza de la persona
    print(clien)
    # Actualiza la información de la persona
    persona.update_persona(idpersona=idper, person=person_dt)
    print("hola") 
    
    try:
        # Actualizar preferencias del cliente en la base de datos
        cursor.execute('''UPDATE cliente SET preferencias = %s
                          WHERE idcliente = %s''',
                       (clien.preferencias, idcliente))
        conn.commit()  # Confirmar los cambios en la base de datos
    except mysql.connector.Error as err:
        conn.rollback()  # Revertir cambios en caso de error
        raise HTTPException(status_code=400, detail=str(err))  # Lanzar una excepción HTTP
    finally:
        conn.close()  # Asegurarse de cerrar la conexión

    return {"message": "Cliente actualizado con éxito"}



def select_personaidcliente(idcliente: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (idcliente,))
    client = cursor.fetchone()
    conn.close()

    if client is None:
        raise HTTPException(status_code=404, detail="persona no encontrada")
    return client["idpersona"]
