import os
from fastapi import HTTPException,UploadFile,File
from database import create_connection
from models.producto import ProductoCreate
from models.tipo import TipoCreate
import mysql.connector
import shutil  # Asegúrate de importar shutil
from cruds import tipo
from typing import Optional
# Crear un nuevo producto
def proceso_guardado(prod: ProductoCreate, file: Optional[UploadFile]):
    
    if file:
        file_location = f"img/{file.filename}"
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        urlimagen = f"http://127.0.0.1:4500/img/{file.filename}"
    else:
        urlimagen = None  # Si no hay imagen, la URL será nula
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    try:
        # Verificar si el tipo existe
        cursor.execute("SELECT * FROM Tipo WHERE idtipo = %s", (prod.idtipo,))
        tipo_existente = cursor.fetchone()

        if tipo_existente is None:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")

        # Insertar el producto en la base de datos
        cursor.execute('''INSERT INTO Producto (idtipo, nombre_producto, stock_producto, unidad_de_medida, precio_producto, urlimagen, estado)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                          (prod.idtipo, prod.nombre_producto, prod.stock_producto, prod.unidad_de_medida, 
                          prod.precio_producto, urlimagen, 1))
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

    cursor.execute('''SELECT p.*, t.nombre_tipo 
                      FROM Producto p
                      JOIN  
                      Tipo t ON p.idtipo = t.idTipo
                      WHERE p.idProducto = %s''', (idproducto,))
    producto = cursor.fetchone()
    conn.close()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto

    
    if file:
        file_location = f"img/{file.filename}"
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        urlimagen = f"http://127.0.0.1:4500/img/{file.filename}"
    else:
        urlimagen = None  # Si no hay imagen, la URL será nula
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    try:
        # Verificar si el tipo existe
        cursor.execute("SELECT * FROM Tipo WHERE idtipo = %s", (prod.idtipo,))
        tipo_existente = cursor.fetchone()

        if tipo_existente is None:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")

        # Insertar el producto en la base de datos
        cursor.execute('''INSERT INTO Producto (idtipo, nombre_producto, stock_producto, unidad_de_medida, precio_producto, urlimagen, estado)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                          (prod.idtipo, prod.nombre_producto, prod.stock_producto, prod.unidad_de_medida, 
                          prod.precio_producto, urlimagen, 1))
        conn.commit()

    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Producto creado con éxito"}

# Actualizar un producto por su ID (permitiendo cambiar de tipo)
def update_producto(idprod: int, producto: ProductoCreate, file: Optional[UploadFile]):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()
    
    urlimagen = None
    try:
        cursor.execute("SELECT * FROM Tipo WHERE idTipo = %s", (producto.idtipo,))
        tipo_existente = cursor.fetchone()

        if tipo_existente is None:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")
        # Si se sube un nuevo archivo, manejar la nueva imagen
        if file:
            file_location = f"img/{file.filename}"
            with open(file_location, "wb") as f:
                shutil.copyfileobj(file.file, f)

            urlimagen = f"http://127.0.0.1:4500/img/{file.filename}"

        # Si no se envía una nueva imagen, mantener la imagen actual
        else:
            cursor.execute("SELECT urlimagen FROM Producto WHERE idproducto = %s", (idprod,))
            producto_actual = cursor.fetchone()

            if producto_actual and producto_actual[0]:
                urlimagen = producto_actual[0]  # Mantener la URL actual de la imagen
            else:
                urlimagen = None  # Si no existe imagen previa, dejarla en `None`

        # Actualizar el producto en la base de datos
        cursor.execute('''UPDATE Producto
                          SET idtipo = %s, nombre_producto = %s, stock_producto = %s, unidad_de_medida = %s, precio_producto = %s, urlimagen = %s
                          WHERE idproducto = %s''',
                          (producto.idtipo, producto.nombre_producto, producto.stock_producto, producto.unidad_de_medida, producto.precio_producto, urlimagen, idprod))
        conn.commit()

    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Producto actualizado con éxito", "idproducto": idprod}
# Eliminar (desactivar) un producto por su ID
def delete_producto(idproducto: int):
    conn = create_connection()
    conn.database = os.getenv("DB_NAME")
    cursor = conn.cursor()

    try:
        cursor.execute('''UPDATE Producto SET estado = 0 WHERE idproducto = %s''', (idproducto,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Producto desactivado con éxito"}
