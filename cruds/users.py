import os
from fastapi import HTTPException
from database import create_connection
import bcrypt
from models.user import UserCreate
import mysql.connector

def create_user(user: UserCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode()

    try:
        cursor.execute('''INSERT INTO users (first_name, last_name, phone, DNI, age, sex, username, email, password, role_id, date_created,state) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(),%s)''',
                       (user.first_name, user.last_name, user.phone, user.DNI, user.age, user.sex, user.username, user.email, hashed_password, user.role_id,user.state))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()  # Cierra el cursor también
        conn.close()

    return {"message": "User created successfully"}

def read_users():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return users

def read_usersByIdRole(role_id:int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE role_id = %s", (role_id,))
    users = cursor.fetchall()
    conn.close()

    return users

def select_user_by_id(client_id: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (client_id,))
    client = cursor.fetchone()
    conn.close()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return client

def update_user(client_id: int, user: UserCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    #hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode()

    try:
        cursor.execute('''UPDATE users SET first_name = %s, last_name = %s, phone = %s, DNI = %s, age = %s, sex = %s,
                          username = %s, email = %s, password = %s, role_id = %s 
                          WHERE id = %s''',
                       (user.first_name, user.last_name, user.phone, user.DNI, user.age, user.sex, user.username, user.email, user.password, user.role_id, client_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()  # Cierra el cursor también
        conn.close()

    return {"message": "Client updated successfully"}

def update_user2(client_id: int, user: UserCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode()

    try:
        cursor.execute('''UPDATE users SET first_name = %s, last_name = %s, phone = %s, DNI = %s, age = %s, sex = %s,
                          username = %s, email = %s, password = %s, role_id = %s 
                          WHERE id = %s''',
                       (user.first_name, user.last_name, user.phone, user.DNI, user.age, user.sex, user.username, user.email, hashed_password, user.role_id, client_id))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()  # Cierra el cursor también
        conn.close()

    return {"message": "Client updated successfully"}

def delete_user(client_id: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        # Actualiza el estado del usuario de 1 a 0
        cursor.execute("UPDATE users SET state = 0 WHERE id = %s", (client_id,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()  # Cierra el cursor también
        conn.close()

    return {"message": "Client deleted successfully"}

def login_users(email, password):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            stored_password = user['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                role_id = user['role_id']
                # Obtener el nombre del rol
                cursor.execute("SELECT name FROM roles WHERE id = %s", (role_id,))
                role = cursor.fetchone()['name']
                
                user_data = {
                    "user_id": user['id'],
                    "username": user['username'],
                    "role": role,
                    "message": "Login successful"
                }
                return user_data
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()  # Cierra el cursor también
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