# Proyecto de Gestión de Gastos

Este proyecto es una aplicación web creada con **FastAPI** para gestionar gastos. Permite registrar, visualizar, eliminar y calcular sumatorios por categoría de los gastos. Además, utiliza MySQL como base de datos y Jinja2 para el renderizado de plantillas HTML.

---

## Tecnologías Utilizadas

- **FastAPI**: Framework para construir APIs web rápidas y modernas.
- **MySQL**: Base de datos relacional para almacenar los gastos.
- **Jinja2**: Motor de plantillas para renderizar el frontend.
- **HTML/CSS**: Interfaz de usuario.
- **JavaScript**: Manejo de interacciones y solicitudes dinámicas.

---

## Instalación

### Requisitos Previos
- Python 3.9 o superior
- MySQL instalado y configurado
- Entorno virtual de Python (opcional pero recomendado)

### Pasos
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/tu_proyecto.git
   cd tu_proyecto
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura la base de datos MySQL:
   - Crea una base de datos llamada `gestion_gastos`.
   - Ejecuta el script SQL para crear la tabla:
     ```sql
     CREATE TABLE gastos (
         id INT AUTO_INCREMENT PRIMARY KEY,
         unidades FLOAT NOT NULL,
         fecha_gasto DATE NOT NULL,
         importe DECIMAL(10, 2) NOT NULL,
         descripcion VARCHAR(500) NOT NULL,
         categoria ENUM('Seguros', 'IBI', 'Comunidad', 'Intereses', 'Consumibles') NOT NULL
     );
     ```

5. Configura las credenciales de MySQL en el archivo `config.py`:
   ```python
   def config():
       return {
           "host": "localhost",
           "user": "tu_usuario",
           "password": "tu_contraseña",
           "database": "gestion_gastos"
       }
   ```

6. Ejecuta la aplicación:
   ```bash
   uvicorn main:app --reload
   ```

7. Accede a la aplicación en tu navegador:
   ```
   http://127.0.0.1:8000
   ```

---

## Características

### 1. Registrar Gastos
- Formulario para ingresar:
  - Descripción
  - Importe
  - Fecha
  - Unidades
  - Categoría

### 2. Mostrar Gastos
- Lista de gastos con:
  - ID
  - Unidades
  - Fecha
  - Importe
  - Descripción
  - Categoría

### 3. Eliminar Gastos
- Botón para eliminar gastos directamente desde la lista.

### 4. Sumatorios por Categoría
- Visualiza el total de gastos agrupados por categoría.

---

## Estructura del Proyecto
```
GASTOSHACIENDA/
├── backend/
│   ├── __pycache__/
│   ├── etc/
│   │   ├── __pycache__/
│   │   ├── config.py
│   ├──__init__.py
│   ├── main.py
│   ├── test.py
├── frontend/
│   ├── css/
│   │   ├── style.css
│   ├── js/
│   │   ├── main.js
│   ├── index.html
├── venv/
├── .env
├── .gitignore
├── requirements.txt
```

---

## Rutas del Backend

### Ruta Principal
- **`GET /`**: Sirve la página principal (`index.html`).

### Registrar Gasto
- **`POST /gastos/add`**: Agrega un nuevo gasto a la base de datos.

### Mostrar Gastos
- **`GET /gastos/show`**: Devuelve todos los gastos en formato JSON.

### Eliminar Gasto
- **`GET /gastos/delete/{id}`**: Elimina un gasto por su ID.

### Sumatorios por Categoría
- **`GET /gastos/sumatorios`**: Devuelve el total de importes agrupados por categoría.

---

## Contacto
Cualquier duda o sugerencia, no dudes en contactarme a [pablo.cabello.hurtado@gmail.com](mailto:pablo.cabello.hurtado@gmail.com).

