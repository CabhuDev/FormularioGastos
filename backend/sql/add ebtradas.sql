INSERT INTO gastos (unidades, fecha_gasto, importe, descripcion, categoria)
VALUES
(1, '2024-01-10', 200.00, 'Pago anual del seguro de hogar', 'Seguros'),
(2, '2024-02-15', 500.00, 'Impuesto IBI del año 2024', 'IBI'),
(3, '2024-03-20', 300.50, 'Gastos de comunidad mensual', 'Comunidad'),
(4, '2024-04-25', 120.75, 'Intereses del préstamo hipotecario', 'Intereses'),
(10, '2024-05-05', 75.00, 'Compra de material de oficina', 'Consumibles'),
(5, '2024-06-10', 180.00, 'Renovación del seguro del coche', 'Seguros'),
(1, '2024-07-15', 600.00, 'IBI del local comercial', 'IBI'),
(8, '2024-08-20', 400.00, 'Reparación en zonas comunes', 'Comunidad'),
(6, '2024-09-25', 250.25, 'Pago de intereses del crédito personal', 'Intereses'),
(15, '2024-10-05', 150.00, 'Compra de consumibles de oficina', 'Consumibles');


select * from gastos;