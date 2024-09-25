import os
from dotenv import load_dotenv
import mysql.connector
import bcrypt
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener los valores de las variables de entorno
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Crear una función para la conexión
def create_connection():
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

# Crear la base de datos si no existe
def create_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.commit()
    conn.close()

# Crear tablas y datos iniciales
def create_tables_and_insert_data():
    conn = create_connection()
    conn.database = database
    cursor = conn.cursor()

    # Crear tabla de rol
    cursor.execute('''CREATE TABLE IF NOT EXISTS Rol(
                        idrol INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_rol VARCHAR(250) NOT NULL UNIQUE,
                        estado_rol INT
                    )''')

    # Crear tabla de personas
    cursor.execute('''CREATE TABLE IF NOT EXISTS Persona (
                        idpersona INT AUTO_INCREMENT PRIMARY KEY,
                        apellidos VARCHAR(250),
                        nombres VARCHAR(250),
                        dni VARCHAR(8) NOT NULL UNIQUE,
                        celular VARCHAR(9),
                        estado INT
                    )''')
    # Crear tabla de Usuario
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuario (
                        idusuario INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(250),
                        password VARCHAR(255),
                        idrol INT,
                        idpersona INT,
                        fechacreacion DATETIME,
                        estado INT,
                        FOREIGN KEY (idpersona) REFERENCES Persona(idpersona),
                        FOREIGN KEY (idrol) REFERENCES Rol(idrol)
                    )''')

    # Insertar roles predeterminados y su estado
    roles = [('admin', 1), ('contador', 1), ('transportista', 1)]
    for rol_nombre, rol_estado in roles:
        cursor.execute('''INSERT INTO Rol (nombre_rol, estado_rol) 
                        SELECT %s, %s 
                        WHERE NOT EXISTS (
                            SELECT 1 FROM Rol WHERE nombre_rol = %s
                        )''', (rol_nombre, rol_estado, rol_nombre))

    # Crear una persona administrativa si no existe
    cursor.execute('''INSERT INTO Persona (apellidos, nombres, dni, celular,estado)
                      SELECT 'admin', 'admin', '11111111', '123456789',1
                      WHERE NOT EXISTS (
                          SELECT 1 FROM Persona WHERE dni = '11111111'
                      )''')

    # Crear contraseña encriptada para el usuario administrador
    password_plain = 'password'
    password_hash = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()

    # Insertar el usuario administrador por defecto si no existe
    cursor.execute('''INSERT INTO Usuario (email, password, idrol, idpersona, fechacreacion, estado) 
                    SELECT 'admin@service.com', %s, (SELECT idrol FROM Rol WHERE nombre_rol = 'admin'), 
                                        (SELECT idpersona FROM Persona WHERE dni = '11111111'), 
                                        NOW(), 1
                    WHERE NOT EXISTS (
                        SELECT 1 FROM Usuario WHERE email = 'admin@service.com'
                    )''', (password_hash,))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    
    # Llamar las funciones al inicio
if __name__ == "__main__":
    create_database()
    create_tables_and_insert_data()
    print("Tablas creadas y datos iniciales insertados correctamente.")
    
