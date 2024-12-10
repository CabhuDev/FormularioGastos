SELECT categoria, SUM(importe) AS total_importe
FROM gastos
GROUP BY categoria;
