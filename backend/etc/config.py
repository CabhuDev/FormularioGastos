from dotenv import load_dotenv
import os

def config():
    # Cargar variables de entorno
    load_dotenv()
    
    # Configuración de la conexión a MySQL usando variables de entorno
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "gestionGastos")
    }
    return db_config