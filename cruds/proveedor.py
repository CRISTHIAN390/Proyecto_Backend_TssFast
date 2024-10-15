import os
from fastapi import HTTPException
from database import create_connection
from models.persona import PersonaCreat
from models.proveedor import ProveedorCreate
import mysql.connector
from cruds import persona,cliente

def create_proveedor(prove: ProveedorCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    
     # Creación de la persona
    person_data  = PersonaCreat(apellidos=prove.apellidos, nombres=prove.nombres, dni=prove.dni, celular=prove.celular, estado=prove.estado)
    persona.create_persona(person_data)     
    
    # Seleccionar idpersona por dni y convertir a entero
    idperson = idperson = int(persona.select_persona_dni(prove.dni))
       
    try:
        cursor.execute('''INSERT INTO proveedor(idpersona, nombre_proveedor, ruc) 
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

def update_proveedor(idprove: int,prove: ProveedorCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    
    person_dt = PersonaCreat(
    apellidos=prove.apellidos, 
    nombres=prove.nombres,    
    dni=prove.dni,              
    celular=prove.celular,     
    estado=1                   
    )
    idper =int(select_personaidproveedor(idprove=idprove))  # Obtener el idpersona del cliente en la base de datos
    
    print(idper) 
    # Actualiza de la persona
    print(prove)
    # Actualiza la información de la persona
    persona.update_persona(idpersona=idper, person=person_dt)
    print("hola") 
    
    try:
        # Actualizar preferencias del cliente en la base de datos
        cursor.execute('''UPDATE proveedor SET nombre_proveedor = %s, ruc = %s
                          WHERE idproveedor = %s''',
                       (prove.nombre_proveedor, prove.ruc, idprove))
        conn.commit()  # Confirmar los cambios en la base de datos
    except mysql.connector.Error as err:
        conn.rollback()  # Revertir cambios en caso de error
        raise HTTPException(status_code=400, detail=str(err))  # Lanzar una excepción HTTP
    finally:
        conn.close()  # Asegurarse de cerrar la conexión

    return {"message": "Cliente actualizado con éxito"}

def select_personaidproveedor(idprove: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (idprove,))
    prove = cursor.fetchone()
    conn.close()

    if prove is None:
        raise HTTPException(status_code=404, detail="persona no encontrada")
    return prove["idpersona"]

def delete_proveedor(idprove: int):
    #corrigue el que envio es idcliente
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    idpersona= int(select_personaidproveedor(idprove=idprove)) 
    try:
        # Actualiza el estado del cliente de 1 a 0 (desactivado)
        cursor.execute('''UPDATE proveedor SET estado = 0
                          WHERE idproveedor = %s
                        
                        ''', (idpersona,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "El proveedor se eliminó con éxito"}