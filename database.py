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
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuario(
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
    
     # Crear tabla de Proveedor
    cursor.execute('''CREATE TABLE IF NOT EXISTS Proveedor (
                        idproveedor INT AUTO_INCREMENT PRIMARY KEY,
                        idpersona INT,
                        nombre_proveedor VARCHAR(250),
                        ruc VARCHAR(255),
                        FOREIGN KEY (idpersona) REFERENCES Persona(idpersona)
                    )''')

    # Crear tabla de Cliente
    cursor.execute('''CREATE TABLE IF NOT EXISTS Cliente (
                        idcliente INT AUTO_INCREMENT PRIMARY KEY,
                        idpersona INT,
                        preferencias VARCHAR(250),
                        FOREIGN KEY (idpersona) REFERENCES Persona(idpersona)
                    )''')
    
    # Crear tabla de Almacen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Almacen (
                        idalmacen INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_almacen VARCHAR(200),
                        ubicacion_almacen VARCHAR(200),
                        descripcion_almacen VARCHAR(200),
                        estado_almacen INT
                    )''')
    
    # Crear tabla de Tipo
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tipo(
                        idtipo INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_tipo VARCHAR(200),
                        estado_tipo INT
                    )''')

    # Crear tabla de Producto   --VARBINARY(10000)Limitar a 10,000 bytes
    cursor.execute('''CREATE TABLE IF NOT EXISTS Producto(
                        idproducto INT AUTO_INCREMENT PRIMARY KEY,
                        idtipo INT,
                        nombre_producto VARCHAR(200),
                        stock_producto INT,
                        unidad_de_medida VARCHAR(20),
                        precio_producto DECIMAL(10,2),
                        urlimagen VARCHAR(200), 
                        estado INT,
                        FOREIGN KEY (idtipo) REFERENCES Tipo(idtipo)
                    )''')
    
    # Crear tabla de Vehiculo

 #   cursor.execute('''CREATE TABLE IF NOT EXISTS Vehiculo (
 #                       idvehiculo INT AUTO_INCREMENT PRIMARY KEY,
 #                       nombre_almacen VARCHAR(200),
 #                       ubicacion_almacen VARCHAR(200),
 #                       descripcion_almacen VARCHAR(200),
 #                       estado_almacen INT
 #                   )''')  

    # Lista de tipos de madera con su estado
    
    
    
    
    tipos_madera = [
        ('Madera Pino', 1),
        ('Madera Cedro', 1),
        ('Madera Tornillo', 1),
        ('Madera Caoba', 1),
        ('Madera Moena', 1),
        ('Madera Catahua', 1),
        ('Madera Lupuna', 1),
        ('Madera Copaiba', 1),
        ('Madera Capirona', 1),
        ('Madera Nogal', 1),
        ('Madera Shihuahuaco', 1),
        ('Madera Cumala', 1),
        ('Madera Estoraque', 1),
        ('Madera Ayahuma', 1),
        ('Madera Palo Santo', 1),
        ('Madera Huayruro', 1),
        ('Madera Balsamo', 1),
        ('Madera Requia', 1),
        ('Madera Quinilla', 1),
        ('Madera Marupa', 1)
    ]
    # Inserción en la tabla Tipo
    for nombre_tipo, estado_tipo in tipos_madera:
        cursor.execute('''INSERT INTO Tipo (nombre_tipo, estado_tipo) 
                        SELECT %s, %s 
                        WHERE NOT EXISTS (
                            SELECT 1 FROM Tipo WHERE nombre_tipo = %s
                        )''', (nombre_tipo, estado_tipo, nombre_tipo))
        
    # Insertar roles predeterminados y su estado
    roles = [('admin', 1), ('contador', 1), ('transportista', 1),('invitado', 1)]
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
    
