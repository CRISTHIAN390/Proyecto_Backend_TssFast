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

    # Crear tabla de roles
    cursor.execute('''CREATE TABLE IF NOT EXISTS roles (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(191) NOT NULL UNIQUE,
                        state INT
                    )''')

    # Crear tabla de clientes (usuarios)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        first_name VARCHAR(191),
                        last_name VARCHAR(191),
                        DNI VARCHAR(8),
                        age INT,
                        sex CHAR(1),
                        phone VARCHAR(12) NOT NULL,
                        username VARCHAR(191) NOT NULL UNIQUE,
                        email VARCHAR(191) NOT NULL UNIQUE,
                        password VARCHAR(191) NOT NULL,
                        role_id INT,
                        date_created DATETIME,
                        state INT,
                        FOREIGN KEY (role_id) REFERENCES roles(id)
                    )''')


    # Roles predeterminados y su estado
    roles = [('admin', 1), ('vigilante', 1), ('transportista', 1)]
    for role_name, role_state in roles:
        cursor.execute('''INSERT INTO roles (name, state) 
                          SELECT %s, %s 
                          WHERE NOT EXISTS (
                              SELECT 1 FROM roles WHERE name = %s
                          ) LIMIT 1''', (role_name, role_state, role_name))
    

    # Crear contraseña encriptada para el usuario administrador
    password_plain = 'password'
    password_hash = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()

    # Insertar usuario administrador por defecto si no existe
    cursor.execute('''INSERT INTO users (first_name, last_name, DNI, age, sex, phone,state, username, email, password, role_id, date_created) 
                      SELECT 'criss', 'vidal', '76362554',25, 'M', '917700319',1, 'admin', 'admin@gmail.com', %s, 
                      (SELECT id FROM roles WHERE name = 'admin'), NOW()
                      WHERE NOT EXISTS (
                          SELECT username FROM users WHERE username = 'admin'
                      )''', (password_hash,))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    
    # Llamar las funciones al inicio
if __name__ == "__main__":
    create_database()
    create_tables_and_insert_data()
    print("Tablas creadas y datos iniciales insertados correctamente.")
    
