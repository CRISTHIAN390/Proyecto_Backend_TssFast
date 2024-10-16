import os
from fastapi import HTTPException
from database import create_connection
from models.producto import ProductoCreate
from models.tipo import TipoCreate
import mysql.connector
from cruds import tipo

# Crear un nuevo producto
def create_producto(producto: ProductoCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        # Verificar si el tipo existe
        cursor.execute("SELECT * FROM Tipo WHERE idTipo = %s", (producto.idtipo,))
        tipo_existente = cursor.fetchone()

        if tipo_existente is None:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")

        # Insertar el producto (asegúrate de que todos los valores están presentes)
        cursor.execute('''INSERT INTO Producto (idtipo, nombre_producto, stock_producto, unidad_de_medida, precio_producto, imagen, estado)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                          (producto.idtipo, producto.nombre_producto, producto.stock_producto, producto.unidad_de_medida, producto.precio_producto, producto.imagen, producto.estado))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Producto creado con éxito"}

# Listar todos los productos
def list_productos():
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''SELECT p.*, t.nombre_tipo FROM Producto p
                      JOIN Tipo t ON p.idtipo = t.idTipo
                      WHERE p.estado != 0;''')  # Solo muestra productos activos
    productos = cursor.fetchall()
    conn.close()
    return productos

# Obtener un producto por su ID
def get_producto(idproducto: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''SELECT p.*, t.nombre_tipo FROM Producto p
                      JOIN Tipo t ON p.idtipo = t.idTipo
                      WHERE p.idProducto = %s''', (idproducto,))
    producto = cursor.fetchone()
    conn.close()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto

# Actualizar un producto por su ID (permitiendo cambiar de tipo)
def update_producto(idproducto: int, producto: ProductoCreate):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        # Verificar si el nuevo tipo existe
        cursor.execute("SELECT * FROM Tipo WHERE idTipo = %s", (producto.idtipo,))
        tipo_existente = cursor.fetchone()

        if tipo_existente is None:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")

        # Actualizar el producto
        cursor.execute('''UPDATE Producto
                          SET idtipo = %s, nombre_producto = %s, stock_producto = %s, unidad_de_medida = %s, precio_producto = %s, imagen = %s, estado = %s
                          WHERE idProducto = %s''',
                          (producto.idtipo, producto.nombre_producto, producto.stock_producto, producto.unidad_de_medida, producto.precio_producto, producto.imagen, producto.estado, idproducto))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Producto actualizado con éxito"}

# Eliminar (desactivar) un producto por su ID
def delete_producto(idproducto: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''UPDATE Producto SET estado = 0 WHERE idProducto = %s''', (idproducto,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Producto desactivado con éxito"}
