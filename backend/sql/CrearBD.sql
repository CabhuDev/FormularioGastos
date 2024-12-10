-- Crear la base de datos
CREATE DATABASE gestionGastos;

-- Crear la tabla de gastos
CREATE TABLE gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Identificador único
    unidades FLOAT NOT NULL,                    -- Número de unidades relacionadas al gasto
    fecha_gasto DATE NOT NULL,                  -- Fecha del gasto
    importe DECIMAL(10, 2) NOT NULL,            -- Importe del gasto (hasta 2 decimales)
    descripcion VARCHAR(500) NOT NULL,          -- Descripción del gasto
    categoria ENUM('Seguros', 'IBI', 'Comunidad', 'Intereses', 'Consumibles') NOT NULL
);


    
