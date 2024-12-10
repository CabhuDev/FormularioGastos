

from etc.config import *

from typing import Annotated
from datetime import datetime
import mysql.connector
from fastapi import FastAPI, HTTPException, Request,Form
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


# Inicializar FastAPI
app = FastAPI()


gastos = []





# Paso 1: Establecer conexión con la base de datos MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()  # Crear cursor para ejecutar consultas
id=17
# Paso 2: Preparar y ejecutar consulta SQL para eliminar gasto por ID
query = "DELETE FROM gastos WHERE id = %s;"
cursor.execute(query,(id,))  # Ejecutar consulta con ID del gasto a eliminar
connection.commit()  # Guardar cambios en la base de datos

# Paso 3: Redirigir a la página principal con mensaje de éxito

print("OK")

cursor.close()      # Primero cerramos el cursor
connection.close()




