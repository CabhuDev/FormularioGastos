"""
Este módulo proporciona una aplicación FastAPI para gestionar gastos con integración de base de datos MySQL.
Rutas:
    - GET /: Sirve la plantilla index.html.
    - POST /gastos/add: Inserta un nuevo gasto en la base de datos.
    - GET /gastos/show: Recupera y devuelve todos los gastos de la base de datos en formato JSON.
Funciones:
    - root(request: Request) -> HTMLResponse: Sirve la plantilla index.html con cookies de mensaje opcionales.
    - agregar_gasto(request: Request, unidades: float, fecha_gasto: str, importe: float, descripcion: str, categoria: str) -> HTMLResponse: Inserta un nuevo gasto en la base de datos y redirige a la ruta raíz con un mensaje de éxito.
    - obtener_gastos() -> JSONResponse: Recupera y devuelve todos los gastos de la base de datos en formato JSON.
Dependencias:
    - FastAPI: Framework web para construir APIs.
    - mysql.connector: Conector de base de datos MySQL.
    - Jinja2Templates: Motor de plantillas para renderizar HTML.
    - StaticFiles: Middleware para servir archivos estáticos.
    - FileResponse, HTMLResponse, RedirectResponse, JSONResponse: Clases de respuesta para diferentes tipos de contenido.
    - HTTPException: Clase de excepción para errores HTTP.
    - Annotated: Tipado para formularios de solicitud.
    - datetime: Módulo para manejar fechas y horas.
"""

from etc.config import *

from typing import Annotated
from datetime import datetime
import mysql.connector
from fastapi import FastAPI, HTTPException, Request,Form,Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,HTMLResponse, RedirectResponse, JSONResponse
from starlette.status import HTTP_302_FOUND

# Configuración de Jinja2 para las plantillas HTML, indicando que se encuentran en el directorio ../frontend
templateJinja2 = Jinja2Templates(directory="../frontend")

# Inicializar FastAPI
app = FastAPI()

# Configuración de la conexión a MySQL
db_config = config()

# Configuración para servir archivos estáticos (CSS, JS, imágenes) desde el directorio ../frontend accesibles en la ruta /frontend
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")


gastos = []
# Agregar una ruta para servir el index.html
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Renderiza la página principal (index.html) y maneja los mensajes flash.
    
    Args:
        request (Request): Objeto de solicitud FastAPI que contiene información
            sobre la petición HTTP actual, incluyendo cookies.
    
    Returns:
        TemplateResponse: Respuesta renderizada del template index.html con:
            - request: Objeto de solicitud requerido por Jinja2
            - mensaje: Mensaje flash almacenado en cookies (éxito/error)
            - tipo_mensaje: Tipo de mensaje para estilización (success/error)
    """
    # Obtener mensajes flash de las cookies
    mensaje = request.cookies.get("mensaje")
    tipo_mensaje = request.cookies.get("tipo_mensaje")
    
    # Renderizar template con contexto
    return templateJinja2.TemplateResponse("index.html", {
        "request": request,
        "mensaje": mensaje,
        "tipo<_mensaje": tipo_mensaje   
        }) 


# Ruta para insertar un gasto
@app.post("/gastos/add", response_class= HTMLResponse)
async def agregar_gasto(
    request: Request,
    unidades: Annotated[float,Form()] , 
    fecha_gasto: Annotated[str,Form()], 
    importe: Annotated[float,Form()], 
    descripcion: Annotated[str,Form()],
    categoria: Annotated[str,Form()]):
    """
    Inserta un nuevo gasto en la base de datos y redirige a la página principal.

    Args:
        request (Request): Objeto de solicitud FastAPI
        unidades (float): Cantidad de unidades del gasto
        fecha_gasto (str): Fecha del gasto en formato YYYY-MM-DD
        importe (float): Importe del gasto
        descripcion (str): Descripción del gasto
        categoria (str): Categoría del gasto

    Returns:
        RedirectResponse: Redirige a la página principal con mensaje de éxito

    Raises:
        HTTPException: Error 500 si hay problemas con la base de datos
    """
    try:
        # 1. Primero nos conectamos a la base de datos MySQL usando la configuración que definimos antes
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()  # El cursor es como un puntero que nos permite ejecutar comandos SQL

        # 2. Convertimos la fecha que recibimos del formulario (que viene como texto) 
        # a un formato de fecha que Python puede entender
        fecha_gasto = datetime.strptime(fecha_gasto, "%Y-%m-%d")  # Ejemplo: "2024-03-14" -> objeto fecha

        # 3. Preparamos la consulta SQL que insertará los datos en la tabla
        # Los %s son marcadores de posición que se reemplazarán con los valores reales
        query = """
            INSERT INTO gastos (unidades, fecha_gasto, importe, descripcion, categoria)
            VALUES (%s, %s, %s, %s,%s)
        """

        # 4. Ejecutamos la consulta SQL, reemplazando los %s con nuestros datos
        cursor.execute(query, 
                        (unidades,      # Número de unidades
                        fecha_gasto,    # Fecha del gasto
                        importe,        # Cantidad de dinero
                        descripcion,    # Descripción del gasto
                        categoria))     # Tipo de gasto

        # 5. Guardamos los cambios en la base de datos
        connection.commit()

        # 6. Preparamos la respuesta para redirigir al usuario a la página principal
        response = RedirectResponse(
            url="/",                    # Volver a la página inicial
            status_code=HTTP_302_FOUND  # Código 302 significa redirección temporal
        )

        # 7. Configuramos mensajes para mostrar al usuario que todo salió bien
        # Estos mensajes se guardan en cookies (pequeños datos en el navegador)
        response.set_cookie(
            key="mensaje",
            value="Operación realizada con éxito",
            max_age=5  # La cookie se borrará después de 5 segundos
        )
        response.set_cookie(
            key="tipo_mensaje",
            value="success",  # Tipo 'success' para mostrar en verde
            max_age=5
        )
        
        return response  # Enviamos la respuesta al navegador


    # 8. Si algo sale mal, capturamos el error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Enviamos un error 500 al navegador

    # 9. Siempre cerramos la conexión a la base de datos, haya error o no
    finally:
        cursor.close()      # Primero cerramos el cursor
        connection.close()  # Luego la conexión




# Ruta para mostrar los datos en el index.html
@app.get("/gastos/show", response_class=JSONResponse)
async def obtener_gastos():
    """
    Recupera todos los gastos de la base de datos.

    Returns:
        JSONResponse: Lista de gastos en formato JSON con los campos:
            - id (int): Identificador único del gasto
            - unidades (float): Cantidad de unidades
            - fecha_gasto (str): Fecha en formato YYYY-MM-DD
            - importe (float): Importe del gasto
            - descripcion (str): Descripción del gasto
            - categoria (str): Categoría del gasto

    Raises:
        JSONResponse: Error 500 si hay problemas con la base de datos
    """
    try:
        # Establecer conexión con la base de datos MySQL usando la configuración
        connection = mysql.connector.connect(**db_config)
        # Crear un cursor para ejecutar consultas SQL
        cursor = connection.cursor()

        # Consulta SQL simple para obtener todos los registros de la tabla gastos
        query = "SELECT * FROM gastos"
        # Ejecutar la consulta
        cursor.execute(query)
        # Obtener todos los resultados de la consulta
        registros = cursor.fetchall()

        # Convertir los registros de la base de datos a formato JSON
        # Crear una lista de diccionarios, cada uno representa un gasto
        gastos = [
            {
                "id": row[0],              # Primera columna: ID del gasto
                "unidades": row[1],        # Segunda columna: Cantidad de unidades
                "fecha_gasto": row[2].strftime("%Y-%m-%d"),  # Tercera columna: Fecha formateada
                "importe": float(row[3]),  # Cuarta columna: Importe convertido a float
                "descripcion": row[4],     # Quinta columna: Descripción del gasto
                "categoria": row[5]        # Sexta columna: Categoría del gasto
            }
            for row in registros          # Hacer esto para cada fila obtenida
        ]

        # Devolver los datos en formato JSON
        return JSONResponse(content=gastos)
    except Exception as e:
        # Si ocurre algún error, devolver mensaje de error en formato JSON
        return JSONResponse(content={"error": str(e)}, status_code=500)    

    finally:
        # Cerrar cursor y conexión sin importar si hubo éxito o error
        # Esto es importante para liberar recursos
        cursor.close()
        connection.close()


@app.get("/gastos/delete/{id}")
async def delete_gasto(id : int):
    """
    Elimina un gasto de la base de datos por su ID.
    
    Args:
        id (int): ID del gasto a eliminar
        
    Returns:
        RedirectResponse: Redirige a la página principal con mensaje de éxito
        
    Raises:
        HTTPException: Error 500 si hay problemas con la base de datos
    """
    try:
        # Paso 1: Establecer conexión con la base de datos MySQL
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()  # Crear cursor para ejecutar consultas

        # Paso 2: Preparar y ejecutar consulta SQL para eliminar gasto por ID
        query = "DELETE FROM gastos WHERE id = %s;"
        cursor.execute(query, (id,))  # Ejecutar consulta con ID del gasto a eliminar
        connection.commit()  # Guardar cambios en la base de datos
        print({"mensaje": f"Gasto con ID {id} eliminado correctamente."})
        # Verificar si se eliminó alguna fila
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Gasto con ID {id} no encontrado.")
        
        # Paso 3: Redirigir a la página principal con mensaje de éxito
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie("mensaje", f"Gasto con ID {id} eliminado correctamente.", max_age=5)
        response.set_cookie("tipo_mensaje", "success", max_age=5)
        return response
    
    except Exception as e:
        # Si hay error, devolver respuesta de error
        raise HTTPException(status_code=500, detail=f"Error al eliminar el gasto: {str(e)}")
    
    finally:
        # Siempre cerrar conexiones, haya error o no
        cursor.close()      # Cerrar cursor primero
        connection.close()  



@app.get("/gastos/sumatorios")
def get_sumatorios():
    """
    Obtiene el sumatorio de gastos agrupados por categoría.
    
    Returns:
        JSONResponse: Lista de diccionarios con:
            - categoria (str): Nombre de la categoría
            - total_importe (float): Suma total de importes por categoría
            
    Raises:
        JSONResponse: Error 500 si hay problemas con la base de datos
    """
    try:
        # Paso 1: Establecer conexión con la base de datos MySQL
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()  # Crear cursor para ejecutar consultas

        # Paso 2: Preparar y ejecutar consulta SQL que suma importes por categoría
        # GROUP BY agrupa los resultados por categoría
        # SUM() calcula la suma total de importes para cada grupo
        query = """
            SELECT categoria, SUM(importe) AS total_importe
            FROM gastos
            GROUP BY categoria;
        """
        cursor.execute(query)  # Ejecutar la consulta
        resultados = cursor.fetchall()  # Obtener todos los resultados

        # Paso 3: Convertir resultados a formato JSON
        # Crear lista de diccionarios con categoría y su total
        sumatorios = [
            {
                "categoria": row[0],                # Primera columna: nombre categoría
                "total_importe": float(row[1])      # Segunda columna: suma total convertida a float
            } for row in resultados
        ]

        # Paso 4: Devolver respuesta en formato JSON
        return JSONResponse(content=sumatorios)

    except Exception as e:
        # Si hay error, devolver respuesta de error
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Siempre cerrar conexiones, haya error o no
        cursor.close()      # Cerrar cursor primero
        connection.close()  # Cerrar conexión después


