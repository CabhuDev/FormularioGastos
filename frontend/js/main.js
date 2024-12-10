/**
 * Función asíncrona que recupera y muestra los datos de gastos en una tabla HTML
 * @async
 * @function mostrarDatos
 * @description Obtiene los datos del servidor y los muestra en una tabla dinámica
 */
async function mostrarDatos() {
    // Obtener referencias a los elementos del DOM
    document.getElementById("mostrarDatosBtn")
    const tabla = document.getElementById("tablaGastos");
    const tbody = tabla.querySelector("tbody");

    // Limpiar cualquier contenido previo en la tabla
    tbody.innerHTML = "";

    try {
        // Hacer la solicitud al backend
        const response = await fetch("/gastos/show");
        // Convertir la respuesta a formato JSON
        const datos = await response.json();

        if (response.ok) {
            // Mostrar la tabla si estaba oculta
            tabla.style.display = "table";

            // Iterar sobre cada gasto y crear filas dinámicamente
            datos.forEach(gasto => {
                // Crear nueva fila
                const fila = document.createElement("tr");
                // Insertar celdas con los datos del gasto
                fila.innerHTML = `
                    <td>${gasto.id}</td>
                    <td>${gasto.unidades}</td>
                    <td>${gasto.fecha_gasto}</td>
                    <td>${gasto.importe}€</td>
                    <td>${gasto.descripcion}</td>
                    <td>${gasto.categoria}</td>
                    <td>
                        <a href="/gastos/delete/${gasto.id}" class="btn-delete">
                            Eliminar
                        </a>
                    </td>
                `;
                // Agregar la fila al cuerpo de la tabla
                tbody.appendChild(fila);
            });
        } else {
            // Mostrar alerta si hay error en la respuesta
            alert("Error al cargar los datos: " + datos.error);
        }
    } catch (error) {
        // Capturar y mostrar cualquier error en la petición0
        alert("Error al realizar la solicitud: " + error.message);
    }
    
}

async function eliminarGasto() {
    document.getElementById("deleteBtn")
    try {
        
        // Hacer la solicitud al backend
        const response = await fetch("/gastos/show");

    } catch (error) {
        alert("Error al realizar la solicitud: " + error.message);
    }
}

/**
 * Obtiene los datos de gastos del servidor y los formatea en un array
 * @returns {Promise<Array>} Array de objetos con los datos de gastos
 */
async function getTabla() {
    try {
        // 1. Realizar petición GET al endpoint /gastos/show
        const response = await fetch("/gastos/show");
        // 2. Convertir la respuesta a formato JSON
        const datos = await response.json();

        if (response.ok) {
            // 3. Si la respuesta es exitosa, transformar los datos
            // Mapear cada gasto a un nuevo objeto con la estructura deseada
            let gastosArray = datos.map(gasto => ({
                id: gasto.id,              // Identificador único
                unidades: gasto.unidades,   // Cantidad de unidades
                fecha_gasto: gasto.fecha_gasto, // Fecha del gasto
                importe: gasto.importe,     // Importe monetario
                descripcion: gasto.descripcion, // Descripción del gasto
                categoria: gasto.categoria   // Categoría del gasto
            }));

            return gastosArray; // 4. Devolver el array formateado

        } else {
            // 5. Si hay error en la respuesta, mostrar alerta
            alert("Error al cargar los datos: " + datos.error);
        }
    } catch (error) {
        // 6. Capturar y mostrar cualquier error en la petición
        alert("Error al realizar la solicitud: " + error.message);
    }
}




/**
 * Recupera y muestra datos sumatorios por categoría de forma asíncrona.
 * 
 * Esta función realiza una solicitud al endpoint "/gastos/sumatorios" para obtener
 * datos sumatorios. Luego procesa los datos y los muestra en formato de lista dentro
 * de un elemento contenedor especificado en la página web.
 * 
 * Los datos mostrados incluyen el nombre de la categoría y el importe total formateado
 * a dos decimales.
 * 
 * Si ocurre un error durante la operación de fetch, se captura y se registra en la consola.
 * 
 * @async
 * @function cargarSumatorios
 * @returns {Promise<void>} Una promesa que se resuelve cuando la operación está completa.
 */
async function cargarSumatorios() {
    document.getElementById("sumatoriosBtn")
    try {
        // Hacer la solicitud al endpoint
        const response = await fetch("/gastos/sumatorios");
        const sumatorios = await response.json();

        // Contenedor donde se mostrarán los sumatorios
        const contenedor = document.getElementById("sumatorios");
        contenedor.innerHTML = "<h3>Sumatorios por Categoría</h3>";

        // Crear la lista de sumatorios
        const lista = document.createElement("ul");
        sumatorios.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.categoria}: ${item.total_importe.toFixed(2)} €`;
            lista.appendChild(li);
        });

        contenedor.appendChild(lista);
    } catch (error) {
        console.error("Error al cargar los sumatorios:", error);
    }
}




//TEST//
// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
    // Vincular el evento 'click' al botón
    const alertButton = document.getElementById("alertButton");

    if (alertButton) {
        alertButton.addEventListener("click", () => {
            alert("Hola Caracola");
        });
    } else {
        console.error("El botón con ID 'alertButton' no se encontró en el DOM.");
    }
});
